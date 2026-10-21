from interfaces.repository import ClinicRepository
from interfaces.services import ClinicServiceInterface, Notifier
from models.entities import Patient, Doctor, Appointment, Diagnosis
from models.enums import AppointmentStatus


class ClinicService(ClinicServiceInterface):

    def __init__(
        self,
        repository: ClinicRepository,
        notifier: Notifier
    ):
        self.repository = repository
        self.notifier = notifier

    def register_patient(self, patient: Patient) -> None:
        if patient.id <= 0:
            raise ValueError("ID пациента должен быть положительным")

        if not patient.name.strip():
            raise ValueError("ФИО пациента не может быть пустым")

        self.repository.add_patient(patient)
        self.notifier.send(f"Пациент {patient.name} зарегистрирован")

    def register_doctor(self, doctor: Doctor) -> None:
        if doctor.id <= 0:
            raise ValueError("ID врача должен быть положительным")

        if not doctor.name.strip():
            raise ValueError("ФИО врача не может быть пустым")

        if not doctor.specialization.strip():
            raise ValueError("Специальность не может быть пустой")

        self.repository.add_doctor(doctor)
        self.notifier.send(f"Врач {doctor.name} зарегистрирован")

    def get_doctors(self) -> list[Doctor]:
        return self.repository.get_all_doctors()

    def create_appointment(
        self,
        appointment_id: int,
        patient_id: int,
        doctor_id: int
    ) -> None:
        if appointment_id <= 0:
            raise ValueError("ID приёма должен быть положительным")

        patient = self.repository.get_patient(patient_id)
        doctor = self.repository.get_doctor(doctor_id)

        if patient is None:
            raise ValueError("Пациент не найден")

        if doctor is None:
            raise ValueError("Врач не найден")

        appointment = Appointment(
            id=appointment_id,
            patient_id=patient_id,
            doctor_id=doctor_id
        )

        self.repository.add_appointment(appointment)

        self.notifier.send(
            f"Пациент {patient.name} записан к врачу {doctor.name}"
        )

    def complete_appointment(
        self,
        appointment_id: int,
        result: str,
        diagnosis_name: str,
        diagnosis_description: str = ""
    ) -> None:
        appointment = self.repository.get_appointment(appointment_id)

        if appointment is None:
            raise ValueError("Приём не найден")

        if appointment.status == AppointmentStatus.COMPLETED:
            raise ValueError("Приём уже завершён")

        if not result.strip():
            raise ValueError("Результат приёма не может быть пустым")

        if not diagnosis_name.strip():
            raise ValueError("Название диагноза не может быть пустым")

        appointment.diagnosis = Diagnosis(
            name=diagnosis_name,
            description=diagnosis_description
        )

        appointment.result = result
        appointment.status = AppointmentStatus.COMPLETED

        self.repository.update_appointment(appointment)

        self.notifier.send(
            f"Приём №{appointment_id} завершён"
        )

    def get_appointments(self) -> list[Appointment]:
        return self.repository.get_all_appointments()

    def get_patient_history(
        self,
        patient_id: int
    ) -> list[Appointment]:
        patient = self.repository.get_patient(patient_id)

        if patient is None:
            raise ValueError("Пациент не найден")

        return self.repository.get_patient_history(patient_id)

    def get_result(self, appointment_id: int) -> str:
        appointment = self.repository.get_appointment(appointment_id)

        if appointment is None:
            raise ValueError("Приём не найден")

        if appointment.status != AppointmentStatus.COMPLETED:
            raise ValueError("Приём ещё не завершён")

        return appointment.result
