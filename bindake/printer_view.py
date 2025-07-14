from lib.message_passer import MessagePasser


class PrinterView(MessagePasser):
    def __init__(self):
        self.tk = None

    def receive(self, message: dict):
        print(f"printer view received, {message}")
