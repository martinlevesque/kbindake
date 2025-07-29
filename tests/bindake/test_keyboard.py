import threading
from dataclasses import dataclass, field

from pynput.keyboard import Key
from bindake.keyboard import MyKeyboard
from lib.message_passer import MessagePasser


@dataclass
class KeyboardTestListener(MessagePasser):
    messages: list[dict] = field(default_factory=list)

    def clear(self):
        self.messages = []

    def receive(self, message: dict):
        self.messages.append(message)


def test_keyboard_happy_path():
    listener = KeyboardTestListener()

    stop_event = threading.Event()
    keyboard = MyKeyboard(notify_to=[listener], stop_event=stop_event)
    listener.clear()

    if keyboard.notify_to:
        keyboard.notify_hotkey("<cmd>+f")

        assert len(listener.messages) == 1
        print(f"listener.message {listener.messages}")
        assert listener.messages == [
            {"origin": "MyKeyboard", "hotkey_pressed": "<cmd>+f"}
        ]

        keyboard.notify_hotkey("<cmd>+c")

        assert len(listener.messages) == 2
        assert listener.messages == [
            {"origin": "MyKeyboard", "hotkey_pressed": "<cmd>+f"},
            {"origin": "MyKeyboard", "hotkey_pressed": "<cmd>+c"},
        ]
