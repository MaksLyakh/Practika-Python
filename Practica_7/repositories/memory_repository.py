from interfaces.repository import ClinicRepository
from models.entities import Patient, Doctor, Appointment
from models.enums import AppointmentStatus


class MemoryClinicRepository(ClinicRepository):

    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.appointments = {}

    def add_patient(self, patient: Patient) -> None:
        if patient.id in self.patients:
            raise ValueError("Пациент с таким ID уже существует")

        self.patients[patient.id] = patient

    def get_patient(self, patient_id: int) -> Patient | None:
        return self.patients.get(patient_id)

    def add_doctor(self, doctor: Doctor) -> None:
        if doctor.id in self.doctors:
            raise ValueError("Врач с таким ID уже существует")

        self.doctors[doctor.id] = doctor

    def get_doctor(self, doctor_id: int) -> Doctor | None:
        return self.doctors.get(doctor_id)

    def get_all_doctors(self) -> list[Doctor]:
        return list(self.doctors.values())

    def add_appointment(self, appointment: Appointment) -> None:
        if appointment.id in self.appointments:
            raise ValueError("Приём с таким ID уже существует")

        self.appointments[appointment.id] = appointment

    def get_appointment(self, appointment_id: int) -> Appointment | None:
        return self.appointments.get(appointment_id)

    def get_all_appointments(self) -> list[Appointment]:
        return list(self.appointments.values())

    def get_patient_history(self, patient_id: int) -> list[Appointment]:
        return [
            appointment
            for appointment in self.appointments.values()
            if appointment.patient_id == patient_id
            and appointment.status == AppointmentStatus.COMPLETED
        ]

    def update_appointment(self, appointment: Appointment) -> None:
        if appointment.id not in self.appointments:
            raise ValueError("Приём не найден")

        self.appointments[appointment.id] = appointment
