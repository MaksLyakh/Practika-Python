from abc import ABC, abstractmethod
from typing import Protocol
from models.entities import Patient, Doctor, Appointment


class ClinicServiceInterface(ABC):

    @abstractmethod
    def register_patient(self, patient: Patient) -> None:
        pass

    @abstractmethod
    def register_doctor(self, doctor: Doctor) -> None:
        pass

    @abstractmethod
    def get_doctors(self) -> list[Doctor]:
        pass

    @abstractmethod
    def create_appointment(
        self,
        appointment_id: int,
        patient_id: int,
        doctor_id: int
    ) -> None:
        pass

    @abstractmethod
    def complete_appointment(
        self,
        appointment_id: int,
        result: str,
        diagnosis_name: str,
        diagnosis_description: str = ""
    ) -> None:
        pass

    @abstractmethod
    def get_appointments(self) -> list[Appointment]:
        pass

    @abstractmethod
    def get_patient_history(
        self,
        patient_id: int
    ) -> list[Appointment]:
        pass

    @abstractmethod
    def get_result(self, appointment_id: int) -> str:
        pass



class Notifier(Protocol):

    def send(self, message: str) -> None:
        ...
