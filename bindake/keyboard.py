import time
import threading
from dataclasses import dataclass, field
from typing import Optional, Any
from .hotkey import normalize_string_hotkey

from lib.message_passer import MessagePasser
from pynput import keyboard

KEY_HISTORY_TIMEOUT = (
    20  # in sec, after this interval the key is removed from the history
)

ALT_L_KEYS = {"<65511>", "alt"}
ALT_R_KEYS = {"<65027>", "alt_r"}


@dataclass
class MyKeyboard(MessagePasser):
    notify_to: Optional[list[MessagePasser]]
    stop_event: threading.Event
    listener: keyboard.Listener | None = None
    hotkeys: list[str] = field(default_factory=list)

    def notify(self, message, destinations: list[MessagePasser]):
        for destination in destinations:
            destination.receive(message)

    def notification_state_message(self, hotkey: str):
        return {
            "origin": "MyKeyboard",
            "hotkey_pressed": hotkey,
        }

    def notify_hotkey(self, hotkey: str):
        self.notify(self.notification_state_message(hotkey), self.notify_to or [])

    def listen(self):
        def on_hotkey(hotkey_name, key_combo):
            normalized_hotkey = normalize_string_hotkey(key_combo)
            self.notify_hotkey(normalized_hotkey)

        def for_canonical(f):
            return lambda k: f(listener.canonical(k))

        def build_hotkey(hotkey: str) -> keyboard.HotKey | None:
            try:
                return keyboard.HotKey(
                    keyboard.HotKey.parse(hotkey),
                    lambda: on_hotkey(hotkey, hotkey),
                )
            except ValueError:
                return None

        hotkeys = []

        for h in self.hotkeys:
            hotkey_object = build_hotkey(h)

            if hotkey_object:
                hotkeys.append(hotkey_object)
            else:
                print(f"Invalid hotkey {h}")

        def on_press(key):
            for hotkey in hotkeys:
                hotkey.press(listener.canonical(key))

        def on_release(key):
            for hotkey in hotkeys:
                hotkey.release(listener.canonical(key))

        with keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
            suppress=False,  # Make sure we don't suppress key events
        ) as listener:
            self.listener = listener
            while not self.stop_event.is_set():
                time.sleep(0.1)

            listener.stop()
