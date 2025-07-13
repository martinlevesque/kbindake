from dataclasses import dataclass
from pynput import keyboard
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Or DEBUG for more detail
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


@dataclass
class Bindake:
    listener: keyboard.Listener

    def info(self, message: str):
        logging.getLogger(__name__).info(message)

    def error(self, message: str):
        logging.getLogger(__name__).error(message)

    def __post_init__(self):
        self.info("Starting Bindake")

    def listen(self):
        self.listener.join()
