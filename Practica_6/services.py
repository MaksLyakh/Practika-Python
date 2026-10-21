from models import Patient, Doctor, Appointment, AppointmentStatus
from decorators import log_call, measure_time


class ClinicError(Exception):
    pass


class Clinic:
    def __init__(self):
        self.patients: list[Patient] = []
        self.doctors: list[Doctor] = []
        self.appointments: list[Appointment] = []

    # Поиск пациента
    def find_patient(self, patient_id: int) -> Patient | None:
        for patient in self.patients:
            if patient.id == patient_id:
                return patient
        return None

    # Поиск врача
    def find_doctor(self, doctor_id: int) -> Doctor | None:
        for doctor in self.doctors:
            if doctor.id == doctor_id:
                return doctor
        return None

    # Поиск приёма
    def find_appointment(self, appointment_id: int) -> Appointment | None:
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                return appointment
        return None

    # Добавление пациента
    @log_call
    def add_patient(self, patient: Patient) -> None:
        if self.find_patient(patient.id) is not None:
            raise ClinicError("Пациент с таким ID уже существует")

        if patient.age <= 0:
            raise ClinicError("Возраст должен быть положительным")

        if not patient.name.strip():
            raise ClinicError("Имя пациента не может быть пустым")

        self.patients.append(patient)

    # Добавление врача
    @log_call
    def add_doctor(self, doctor: Doctor) -> None:
        if self.find_doctor(doctor.id) is not None:
            raise ClinicError("Врач с таким ID уже существует")

        if not doctor.name.strip() or not doctor.specialization.strip():
            raise ClinicError("Имя и специальность врача не могут быть пустыми")

        self.doctors.append(doctor)

    # Добавление приёма
    @log_call
    def add_appointment(self, appointment: Appointment) -> None:
        if self.find_appointment(appointment.id) is not None:
            raise ClinicError("Приём с таким ID уже существует")

        if self.find_patient(appointment.patient_id) is None:
            raise ClinicError("Пациент не найден")

        if self.find_doctor(appointment.doctor_id) is None:
            raise ClinicError("Врач не найден")

        if appointment.duration <= 0:
            raise ClinicError("Продолжительность должна быть больше нуля")

        self.appointments.append(appointment)

    # Удаление пациента
    def delete_patient(self, patient_id: int) -> None:
        patient = self.find_patient(patient_id)

        if patient is None:
            raise ClinicError("Пациент не найден")

        for appointment in self.appointments:
            if appointment.patient_id == patient_id:
                raise ClinicError("Нельзя удалить пациента, у которого есть приёмы")

        self.patients.remove(patient)

    # Удаление врача
    def delete_doctor(self, doctor_id: int) -> None:
        doctor = self.find_doctor(doctor_id)

        if doctor is None:
            raise ClinicError("Врач не найден")

        for appointment in self.appointments:
            if appointment.doctor_id == doctor_id:
                raise ClinicError("Нельзя удалить врача, у которого есть приёмы")

        self.doctors.remove(doctor)

    # Удаление приёма
    def delete_appointment(self, appointment_id: int) -> None:
        appointment = self.find_appointment(appointment_id)

        if appointment is None:
            raise ClinicError("Приём не найден")

        self.appointments.remove(appointment)

    # Изменение статуса приёма
    @log_call
    def change_status(
        self, appointment_id: int, new_status: AppointmentStatus
    ) -> None:
        appointment = self.find_appointment(appointment_id)

        if appointment is None:
            raise ClinicError("Приём не найден")

        allowed = {
            AppointmentStatus.PLANNED: [
                AppointmentStatus.CONFIRMED,
                AppointmentStatus.CANCELLED
            ],
            AppointmentStatus.CONFIRMED: [
                AppointmentStatus.COMPLETED,
                AppointmentStatus.CANCELLED
            ],
            AppointmentStatus.COMPLETED: [],
            AppointmentStatus.CANCELLED: []
        }

        if new_status not in allowed[appointment.status]:
            raise ClinicError("Недопустимое изменение статуса")

        appointment.status = new_status

    # Подсчёт приёмов определённого врача
    def count_doctor_appointments(self, doctor_id: int) -> int:
        if self.find_doctor(doctor_id) is None:
            raise ClinicError("Врач не найден")

        count = 0

        for appointment in self.appointments:
            if appointment.doctor_id == doctor_id:
                count += 1

        return count

    # Средняя продолжительность приёма
    def average_duration(self) -> float:
        if len(self.appointments) == 0:
            return 0.0

        total = 0

        for appointment in self.appointments:
            total += appointment.duration

        return total / len(self.appointments)

    # Формирование статистики
    @measure_time
    def get_statistics(self) -> dict[str, int | float]:
        planned = 0
        confirmed = 0
        completed = 0
        cancelled = 0

        for appointment in self.appointments:
            if appointment.status == AppointmentStatus.PLANNED:
                planned += 1
            elif appointment.status == AppointmentStatus.CONFIRMED:
                confirmed += 1
            elif appointment.status == AppointmentStatus.COMPLETED:
                completed += 1
            elif appointment.status == AppointmentStatus.CANCELLED:
                cancelled += 1

        return {
            "Пациентов": len(self.patients),
            "Врачей": len(self.doctors),
            "Всего приёмов": len(self.appointments),
            "Запланировано": planned,
            "Подтверждено": confirmed,
            "Завершено": completed,
            "Отменено": cancelled,
            "Средняя продолжительность": self.average_duration()
        }
