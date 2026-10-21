class ConsoleNotifier:

    def send(self, message: str) -> None:
        print(f"[Уведомление] {message}")


class SilentNotifier:

    def send(self, message: str) -> None:
        pass
