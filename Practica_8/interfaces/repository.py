from typing import Protocol
from models.entities import Appointment


class AppointmentRepository(Protocol):

    def add(self, appointment: Appointment) -> None:
        ...

    def get(self, appointment_id: int) -> Appointment | None:
        ...

    def get_all(self) -> list[Appointment]:
        ...

    def delete(self, appointment_id: int) -> None:
        ...
