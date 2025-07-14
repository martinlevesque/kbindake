from dataclasses import dataclass
from tkinter import Message
from typing import Optional
from lib.message_passer import MessagePasser
import pynput


@dataclass
class MyKeyboard(MessagePasser):
    notify_to: Optional[list[MessagePasser]]

    def __postinit__(self):
        self.current_keys = set()

    def on_press(self, key):
        # self.receive({"action": "press", "keycode": key})
        print("on prress keyboard, key = ", key)

    def on_release(self, key):
        # my_keyboard.receive({"action": "release", "keycode": key})
        print("on release keyboard, key = ", key)
        if str(key) == "Key.shift_r" and self.notify_to:
            self.send({ "status": "ok", "origin": self }, self.notify_to)

    def receive(self, message: dict):
        print(f"my keyboard .. msg received {message}")

    def send(self, message, destinations: list[MessagePasser]):
        for destination in destinations:
            destination.receive({"origine": "MyKeyboard", "status": "ok"})

    def listen(self):
        with pynput.keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        ) as listener:
            listener.join()
