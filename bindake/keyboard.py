import copy
import time
import threading
from functools import lru_cache
from dataclasses import dataclass, field
from typing import Optional

from lib.message_passer import MessagePasser
import pynput

KEY_HISTORY_TIMEOUT = 10  # in sec, after this interval the key is from the history

ALT_L_KEYS = {"<65511>", "alt"}
ALT_R_KEYS = {"<65027>", "alt_r"}


@dataclass(frozen=True)
class KeyboardKey:
    key: str
    t: float = time.time()

    def __eq__(self, other):
        if not isinstance(other, KeyboardKey):
            return NotImplemented

        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return self.key


@dataclass
class MyKeyboard(MessagePasser):
    notify_to: Optional[list[MessagePasser]]
    stop_event: threading.Event
    current_keys: list[KeyboardKey] = field(default_factory=list)
    listener: pynput.keyboard.Listener | None = None

    def notify(self, message, destinations: list[MessagePasser]):
        for destination in destinations:
            destination.receive(message)

    def on_press(self, key):
        new_keyboard_key = KeyboardKey(key=MyKeyboard.normalize_key(key), t=time.time())

        if new_keyboard_key not in self.current_keys:
            self.current_keys.append(new_keyboard_key)

        self.garbage_collect()
        self.notify(self.notification_state_message(), self.notify_to or [])

    def on_release(self, key):
        keyboard_key_to_remove = KeyboardKey(
            key=MyKeyboard.normalize_key(key), t=time.time()
        )

        if keyboard_key_to_remove in self.current_keys:
            self.current_keys.remove(keyboard_key_to_remove)

        self.garbage_collect()
        self.notify(self.notification_state_message(), self.notify_to or [])

    @staticmethod
    @lru_cache(maxsize=1)
    def keys() -> tuple[str, ...]:
        result = []

        special_keys = [MyKeyboard.normalize_key(k) for k in list(pynput.keyboard.Key)]

        # Printable character keys (you can expand as needed)
        char_keys = [chr(c) for c in range(32, 127)]  # from space to ~ (ASCII)

        return tuple(special_keys + char_keys)

    @staticmethod
    def valid_key(key: str) -> bool:
        return key in MyKeyboard.keys()

    def normalized_current_keys(self):
        return sorted([k.key.strip().lower() for k in self.current_keys])

    def notification_state_message(self):
        return {
            "origin": "MyKeyboard",
            "current_keys": self.normalized_current_keys(),
        }

    def garbage_collect(self):
        expired = {
            k for k in self.current_keys if time.time() - k.t > KEY_HISTORY_TIMEOUT
        }

        for k in expired:
            self.current_keys.remove(k)

    @staticmethod
    def normalize_key(key) -> str:
        s_key = (
            str(key)
            .removeprefix("Key.")
            .replace("'", "")
            .replace("_", " ")
            .capitalize()
        )

        return s_key

    def listen(self):
        with pynput.keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        ) as listener:
            while not self.stop_event.is_set():
                time.sleep(0.1)

            listener.stop()
