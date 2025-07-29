from dataclasses import dataclass
import logging
import sys
import threading

from bindake.makefile_config import MakefileConfig
from bindake.arg_settings import ArgSettings
from lib.message_passer import MessagePasser

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Or DEBUG for more detail
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
from .keyboard import MyKeyboard
from .printer_view import PrinterView


@dataclass
class Bindake(MessagePasser):
    my_keyboard: MyKeyboard
    view: PrinterView
    stop_event: threading.Event
    settings: ArgSettings
    makefile: MakefileConfig | None = None

    def info(self, message: str):
        logging.getLogger(__name__).info(message)

    def error(self, message: str):
        logging.getLogger(__name__).error(message)

    def verbose_info(self, message: str):
        if self.settings.verbose:
            self.info(message)

    def __post_init__(self):
        self.info("Starting Bindake")

    def receive(self, message: dict):
        if not self.makefile:
            self.error("No makefile yet")
            return

        if "hotkey_pressed" not in message:
            self.verbose_info(f"Hotkey pressed but skipping, {message}")
            return

        print(f"received {message}")
        hotkey = message["hotkey_pressed"]

        self.verbose_info(f"Hotkey receive, {hotkey}")

        if self.makefile.bindings.get(hotkey, None):
            binding = self.makefile.bindings[hotkey]
            command = binding.command
            self.verbose_info(
                f"   - key has a binding, command={command}, executing..."
            )
            self.execute_command(binding, command)
        elif hotkey == self.settings.bindings_overlay_hotkey:
            output = ""

            for keys, binding in self.makefile.bindings.items():
                output += f"{binding.command}: {keys}\n"

            self.view.show(output)

    def execute_command(self, binding, command: str):
        if not self.makefile:
            return

        result = self.makefile.execute(command)

        if result["status_code"] == 0:
            self.verbose_info(f"   [+] successful execution")

            display_content = ""

            if binding.overlay_command_output:
                display_content = f"{result['stdout']}".strip()
            else:
                display_content = command

            self.view.show(display_content)
        else:
            output = f"{result['stdout']} {result['stderr']}"
            self.verbose_info(f"   [-] erroneous execution")
            self.view.show(output)

    def destroy(self):
        self.stop_event.set()
        self.view.destroy()

    def loop(self):
        self.my_keyboard.listen()
