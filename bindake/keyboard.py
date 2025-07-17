import copy
import time
from dataclasses import dataclass, field
from typing import Optional

from lib.message_passer import MessagePasser
import pynput

KEY_HISTORY_TIMEOUT = 10  # in sec, after this interval the key is from the history

ALT_L_KEYS = {"<65511>", "alt"}
ALT_R_KEYS = {"<65027>", "alt_r"}


@dataclass(frozen=True)
class CurrentKeyboardKey:
    key: str
    t: float = time.time()

    def __eq__(self, other):
        if not isinstance(other, CurrentKeyboardKey):
            return NotImplemented

        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return self.key


@dataclass
class MyKeyboard(MessagePasser):
    notify_to: Optional[list[MessagePasser]]
    current_keys: set[CurrentKeyboardKey] = field(default_factory=set)

    def receive(self, message: dict):
        print(f"my keyboard .. msg received {message}")

    def notify(self, message, destinations: list[MessagePasser]):
        for destination in destinations:
            destination.receive(message)

    def on_press(self, key):
        self.current_keys.add(
            CurrentKeyboardKey(key=self.strip_key(key), t=time.time())
        )

        self.garbage_collect()
        self.notify(self.notification_state_message(), self.notify_to or [])

    def on_release(self, key):
        self.current_keys.discard(
            CurrentKeyboardKey(key=self.strip_key(key), t=time.time())
        )

        self.garbage_collect()
        self.notify(self.notification_state_message(), self.notify_to or [])

    def notification_state_message(self):
        simplified_keys = set()

        for k in self.current_keys:
            simplified_keys.add(k.key)

        return {
            "origin": "MyKeyboard",
            "current_keys": simplified_keys,
        }

    def garbage_collect(self):
        expired = {
            k for k in self.current_keys if time.time() - k.t > KEY_HISTORY_TIMEOUT
        }
        self.current_keys.difference_update(expired)

    def strip_key(self, key) -> str:
        s_key = str(key).removeprefix("Key.").replace("'", "")

        return s_key

    def listen(self):
        with pynput.keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        ) as listener:
            listener.join()
