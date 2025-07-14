from dataclasses import dataclass
from typing import Optional
import pynput
import logging

from lib.message_passer import MessagePasser

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Or DEBUG for more detail
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
from .keyboard import MyKeyboard
from .printer_view import PrinterView

view = PrinterView()


@dataclass
class Bindake(MessagePasser):
    my_keyboard: Optional[MyKeyboard] = None
    view: Optional[PrinterView] = None

    def info(self, message: str):
        logging.getLogger(__name__).info(message)

    def error(self, message: str):
        logging.getLogger(__name__).error(message)

    def __post_init__(self):
        self.info("Starting Bindake")

    def receive(self, message: dict):
        print(f"bindake recv: {message}")

    def loop(self):
        if self.my_keyboard:
            self.my_keyboard.listen()
