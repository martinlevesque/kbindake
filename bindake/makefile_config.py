from dataclasses import dataclass, field
from typing import Dict, Any, FrozenSet
import re
import subprocess

from bindake.keyboard import KeyboardKey


@dataclass
class Binding:
    command: str
    autoboot: bool = False
    overlay_command_output: bool = False


@dataclass
class MakefileConfig:
    filepath: str
    bindings: Dict[str, Binding] = field(default_factory=dict)

    def read_file_lines(self):
        with open(self.filepath, "r", encoding="utf-8") as file:
            return file.readlines()

    def parse_bindings(self, line):
        match = re.match(
            r"^#\s*bindake(\[((overlay-command-output|autoboot),?)*\])?:\s*(.+)$",
            line,
        )

        if match:
            options_str = match.group(0)
            command_str = match.group(4)
            commands = [cmd.strip().lower() for cmd in command_str.split("+")]

            return {
                "commands": commands,
                "autoboot": "autoboot" in options_str,
                "overlay_command_output": "overlay-command-output" in options_str,
            }

        return None

    @staticmethod
    def human_key_to_normalized(input: str) -> str:
        keys = input.strip().lower().split("+")

        return "+".join(sorted(keys))

    def parse_command(self, line):
        match = re.match(r"^\s*([A-Za-z0-9_\-./]+)\s*:\s*(.*)?$", line)

        if match:
            return match.group(1)

        return None

    def parse(self):
        lines = self.read_file_lines()
        previous_line = None
        self.bindings = {}

        for i, line in enumerate(lines):
            if previous_line is not None:
                binding = self.parse_bindings(previous_line)

                if binding:
                    command = self.parse_command(line)

                    if command:
                        keys = "+".join(sorted(binding["commands"]))
                        self.bindings[keys] = Binding(
                            command=command,
                            autoboot=binding["autoboot"],
                            overlay_command_output=binding["overlay_command_output"],
                        )

            previous_line = line

        return self.bindings

    def execute(self, command):
        result = subprocess.run(
            ["make", "-s", "-f", self.filepath, command], capture_output=True, text=True
        )

        status_code = result.returncode
        stdout = result.stdout
        stderr = result.stderr

        return {"status_code": status_code, "stdout": stdout, "stderr": stderr}
