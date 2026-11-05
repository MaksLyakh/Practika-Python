from typing import Optional

from app.models import Appointment
from app.exceptions import AppointmentNotFoundError


class AppointmentRepository:
    def __init__(self):
        self._appointments: dict[int, Appointment] = {}
        self._next_id = 1

    def get_all(self) -> list[Appointment]:
        return list(self._appointments.values())

    def get_by_id(self, appointment_id: int) -> Appointment:
        appointment = self._appointments.get(appointment_id)

        if appointment is None:
            raise AppointmentNotFoundError(appointment_id)

        return appointment

    def create(self, data: dict) -> Appointment:
        appointment = Appointment(
            id=self._next_id,
            patient=data["patient"],
            doctor=data["doctor"],
            specialty=data["specialty"],
            date=data["date"],
            time=data["time"],
            room=data["room"],
            status=data.get("status", "запланирован")
        )

        self._appointments[self._next_id] = appointment
        self._next_id += 1

        return appointment

    def update(self, appointment_id: int, data: dict) -> Appointment:
        appointment = self.get_by_id(appointment_id)

        for field, value in data.items():
            if field != "id" and hasattr(appointment, field):
                setattr(appointment, field, value)

        return appointment

    def delete(self, appointment_id: int) -> None:
        self.get_by_id(appointment_id)
        del self._appointments[appointment_id]

    def find_by_doctor(self, doctor: str) -> list[Appointment]:
        return [
            appointment
            for appointment in self._appointments.values()
            if appointment.doctor.lower() == doctor.lower()
        ]

    def find_by_status(self, status: str) -> list[Appointment]:
        return [
            appointment
            for appointment in self._appointments.values()
            if appointment.status.lower() == status.lower()
        ]

    def find_by_date(self, date: str) -> list[Appointment]:
        return [
            appointment
            for appointment in self._appointments.values()
            if appointment.date == date
        ]

    def find_by_patient(self, patient: str) -> list[Appointment]:
        return [
            appointment
            for appointment in self._appointments.values()
            if patient.lower() in appointment.patient.lower()
        ]

    def count_by_doctor(self, doctor: str) -> int:
        return len(self.find_by_doctor(doctor))

    def clear(self) -> None:
        self._appointments.clear()
        self._next_id = 1
