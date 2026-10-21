from typing import Protocol


class Observer(Protocol):

    def update(self, message: str) -> None:
        ...


class ConsoleObserver:

    def update(self, message: str) -> None:
        print(f"Уведомление: {message}")


class AppointmentNotifier:

    def __init__(self):
        self.observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self.observers.append(observer)

    def notify(self, message: str) -> None:
        for observer in self.observers:
            observer.update(message)
