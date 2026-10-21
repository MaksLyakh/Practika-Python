from models.entities import Appointment


class MemoryAppointmentRepository:

    def __init__(self):
        self.appointments: dict[int, Appointment] = {}

    def add(self, appointment: Appointment) -> None:
        if appointment.id in self.appointments:
            raise ValueError("Запись с таким ID уже существует")

        self.appointments[appointment.id] = appointment

    def get(self, appointment_id: int) -> Appointment | None:
        return self.appointments.get(appointment_id)

    def get_all(self) -> list[Appointment]:
        return list(self.appointments.values())

    def delete(self, appointment_id: int) -> None:
        if appointment_id not in self.appointments:
            raise ValueError("Запись не найдена")

        del self.appointments[appointment_id]
