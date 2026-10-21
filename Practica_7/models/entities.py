from dataclasses import dataclass
from models.enums import AppointmentStatus


@dataclass
class Patient:
    id: int
    name: str


@dataclass
class Doctor:
    id: int
    name: str
    specialization: str


@dataclass
class Diagnosis:
    name: str
    description: str = ""


@dataclass
class Appointment:
    id: int
    patient_id: int
    doctor_id: int
    status: AppointmentStatus = AppointmentStatus.PLANNED
    result: str = ""
    diagnosis: Diagnosis | None = None
