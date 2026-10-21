from abc import ABC, abstractmethod
from models.entities import Patient, Doctor, Appointment


class ClinicRepository(ABC):

    @abstractmethod
    def add_patient(self, patient: Patient) -> None:
        pass

    @abstractmethod
    def get_patient(self, patient_id: int) -> Patient | None:
        pass

    @abstractmethod
    def add_doctor(self, doctor: Doctor) -> None:
        pass

    @abstractmethod
    def get_doctor(self, doctor_id: int) -> Doctor | None:
        pass

    @abstractmethod
    def get_all_doctors(self) -> list[Doctor]:
        pass

    @abstractmethod
    def add_appointment(self, appointment: Appointment) -> None:
        pass

    @abstractmethod
    def get_appointment(self, appointment_id: int) -> Appointment | None:
        pass

    @abstractmethod
    def get_all_appointments(self) -> list[Appointment]:
        pass

    @abstractmethod
    def get_patient_history(self, patient_id: int) -> list[Appointment]:
        pass

    @abstractmethod
    def update_appointment(self, appointment: Appointment) -> None:
        pass
