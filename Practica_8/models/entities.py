from dataclasses import dataclass
from models.enums import AppointmentType, AppointmentStatus


@dataclass
class Patient:
    id: int
    name: str


@dataclass
class Doctor:
    id: int
    name: str


@dataclass
class Appointment:
    id: int
    patient: Patient
    doctor: Doctor
    appointment_type: AppointmentType
    price: float
    status: AppointmentStatus = AppointmentStatus.PLANNED
