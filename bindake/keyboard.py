import copy
from dataclasses import dataclass, field
from typing import Optional

from pynput.keyboard import KeyCode

from lib.message_passer import MessagePasser
import pynput


@dataclass
class MyKeyboard(MessagePasser):
    notify_to: Optional[list[MessagePasser]]
    current_keys: set[str] = field(default_factory=set)

    def receive(self, message: dict):
        print(f"my keyboard .. msg received {message}")

    def notify(self, message, destinations: list[MessagePasser]):
        for destination in destinations:
            destination.receive(message)

    def on_press(self, key):
        self.current_keys.add(str(key))

        self.notify(self.notification_state_message(), self.notify_to or [])

    def notification_state_message(self):
        return {
            "origin": "MyKeyboard",
            "current_keys": copy.deepcopy(self.current_keys),
        }

    def on_release(self, key):
        self.current_keys.discard(str(key))

        self.notify(self.notification_state_message(), self.notify_to or [])

    def listen(self):
        with pynput.keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        ) as listener:
            listener.join()
