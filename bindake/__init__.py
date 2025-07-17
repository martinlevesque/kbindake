from dataclasses import dataclass
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
    my_keyboard: MyKeyboard
    view: PrinterView

    def info(self, message: str):
        logging.getLogger(__name__).info(message)

    def error(self, message: str):
        logging.getLogger(__name__).error(message)

    def __post_init__(self):
        self.info("Starting Bindake")

    def receive(self, message: dict):
        print(f"bindake recv: {message}")
        keys = message["current_keys"]

        if len(keys) > 0:
            self.view.show(f" reccvv {message['current_keys']}")

    def loop(self):
        self.my_keyboard.listen()
