from dataclasses import dataclass, field
from typing import Dict, Any, FrozenSet
import re
import subprocess

from kbindake import logger
from kbindake import hotkey


@dataclass
class Binding:
    command: str
    original_hotkey: str
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
            r"^#\s*kbindake(\[((overlay-command-output|autoboot),?)*\])?:\s*(.+)$",
            line,
        )

        if match:
            options_str = match.group(0)
            command_str = str(match.group(4))
            commands = hotkey.normalize_string_hotkey_to_list(command_str)

            return {
                "commands": commands,
                "original_commands": command_str,
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

                        if keys in self.bindings:
                            logger.warning(f"Hotkey {keys} already exists! Overriding.")

                        self.bindings[keys] = Binding(
                            command=command,
                            autoboot=binding["autoboot"],
                            overlay_command_output=binding["overlay_command_output"],
                            original_hotkey=binding["original_commands"],
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
