import time
import threading
from dataclasses import dataclass, field
from typing import Optional, Any
from .hotkey import normalize_string_hotkey

from bindake import logger
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

    def validate_hotkey(self, hotkey: str) -> bool:
        try:
            # Try to create a temporary GlobalHotKeys instance to validate the hotkey
            test_dict = {hotkey: lambda: None}
            # This will raise an exception if the hotkey format is invalid
            with keyboard.GlobalHotKeys(test_dict) as test_listener:
                pass  # If we get here, the hotkey is valid
            return True
        except (ValueError, KeyError, AttributeError) as e:
            logger.error(f"Invalid hotkey '{hotkey}': {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error validating hotkey '{hotkey}': {e}")
            return False

    def listen(self):
        def on_hotkey(hotkey_name, key_combo):
            normalized_hotkey = normalize_string_hotkey(key_combo)
            self.notify_hotkey(normalized_hotkey)

        # Build hotkey dictionary for GlobalHotKeys
        hotkey_dict = {}

        for h in self.hotkeys:
            if self.validate_hotkey(h):
                # Parse the hotkey string and create the callback
                hotkey_dict[h] = lambda hotkey=h: on_hotkey(hotkey, hotkey)

        # Use GlobalHotKeys which handles suppression automatically
        with keyboard.GlobalHotKeys(hotkey_dict) as hotkey_listener:
            while not self.stop_event.is_set():
                time.sleep(0.1)
