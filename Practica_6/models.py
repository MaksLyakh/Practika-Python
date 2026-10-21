from dataclasses import dataclass
from enum import Enum


class AppointmentStatus(Enum):
    PLANNED = "Запланирован"
    CONFIRMED = "Подтверждён"
    COMPLETED = "Завершён"
    CANCELLED = "Отменён"


@dataclass
class Person:
    id: int
    name: str


@dataclass
class Patient(Person):
    age: int

    def get_report_data(self) -> str:
        return f"Пациент: {self.name}, возраст: {self.age}"


@dataclass
class Doctor(Person):
    specialization: str

    def get_report_data(self) -> str:
        return f"Врач: {self.name}, специальность: {self.specialization}"


@dataclass
class Appointment:
    id: int
    patient_id: int
    doctor_id: int
    duration: int
    status: AppointmentStatus = AppointmentStatus.PLANNED
