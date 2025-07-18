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
        keyboard.on_press(Key.ctrl_r)

        assert len(listener.messages) == 1
        assert listener.messages == [
            {"origin": "MyKeyboard", "current_keys": {"ctrl_r"}}
        ]

        keyboard.on_press(Key.ctrl)

        assert len(listener.messages) == 2
        assert listener.messages == [
            {"origin": "MyKeyboard", "current_keys": {"ctrl_r"}},
            {"origin": "MyKeyboard", "current_keys": {"ctrl_r", "ctrl"}},
        ]

        listener.clear()

        keyboard.on_release(Key.ctrl)
        assert len(listener.messages) == 1
        assert listener.messages == [
            {"origin": "MyKeyboard", "current_keys": {"ctrl_r"}}
        ]
