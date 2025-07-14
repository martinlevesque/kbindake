class MessagePasser:
    def receive(self, _message: dict) -> None:
        raise NotImplemented

    def notify(self, _message: dict, _destinations: list["MessagePasser"]) -> None:
        raise NotImplemented
