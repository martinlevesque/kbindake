import time
import threading
from dataclasses import dataclass, field
from typing import Optional, Any
from .hotkey import normalize_string_hotkey

from lib.message_passer import MessagePasser
from pynput import keyboard


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

        # Build hotkey dictionary for GlobalHotKeys
        hotkey_dict = {}

        for h in self.hotkeys:
            try:
                # Parse the hotkey string and create the callback
                hotkey_dict[h] = lambda hotkey=h: on_hotkey(hotkey, hotkey)
            except ValueError:
                print(f"Invalid hotkey {h}")

        # Use GlobalHotKeys which handles suppression automatically
        with keyboard.GlobalHotKeys(hotkey_dict) as hotkey_listener:
            while not self.stop_event.is_set():
                time.sleep(0.1)
