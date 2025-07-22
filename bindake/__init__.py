from dataclasses import dataclass
import logging
import sys
import threading

from bindake.makefile_config import MakefileConfig
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
    makefile: MakefileConfig | None = None

    def info(self, message: str):
        logging.getLogger(__name__).info(message)

    def error(self, message: str):
        logging.getLogger(__name__).error(message)

    def __post_init__(self):
        self.info("Starting Bindake")

    def receive(self, message: dict):
        keys = message["current_keys"]
        keys_str = "+".join(keys)

        if self.makefile and self.makefile.bindings.get(keys_str, None):
            self.view.show(self.makefile.bindings[keys_str].command)

    def destroy(self):
        self.stop_event.set()
        self.view.destroy()

    def loop(self):
        self.my_keyboard.listen()
