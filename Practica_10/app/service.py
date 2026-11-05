from datetime import datetime

from app.models import Appointment, APPOINTMENT_STATUSES
from app.repository import AppointmentRepository
from app.exceptions import (
    AppointmentValidationError,
    AppointmentConflictError
)


class AppointmentService:
    FIELDS = (
        "patient",
        "doctor",
        "specialty",
        "date",
        "time",
        "room",
        "status"
    )

    def __init__(self, repository: AppointmentRepository):
        self.repository = repository

    def validate_data(self, data: dict, partial: bool = False) -> None:
        if not isinstance(data, dict):
            raise AppointmentValidationError(
                "Данные должны быть объектом JSON"
            )

        unknown_fields = set(data) - set(self.FIELDS)

        if unknown_fields:
            raise AppointmentValidationError(
                f"Неизвестные поля: {', '.join(sorted(unknown_fields))}"
            )

        required_fields = (
            "patient", "doctor", "specialty",
            "date", "time", "room"
        )

        if not partial:
            missing = [
                field for field in required_fields
                if field not in data
            ]

            if missing:
                raise AppointmentValidationError(
                    f"Отсутствуют обязательные поля: {', '.join(missing)}"
                )

        for field in ("patient", "doctor", "specialty"):
            if field in data:
                value = data[field]

                if not isinstance(value, str) or not value.strip():
                    raise AppointmentValidationError(
                        f"Поле '{field}' должно быть непустой строкой"
                    )

        if "date" in data:
            try:
                datetime.strptime(data["date"], "%Y-%m-%d")
            except (ValueError, TypeError):
                raise AppointmentValidationError(
                    "Дата должна иметь формат YYYY-MM-DD"
                )

        if "time" in data:
            try:
                datetime.strptime(data["time"], "%H:%M")
            except (ValueError, TypeError):
                raise AppointmentValidationError(
                    "Время должно иметь формат HH:MM"
                )

        if "room" in data:
            room = data["room"]

            if type(room) is not int or room <= 0:
                raise AppointmentValidationError(
                    "Номер кабинета должен быть положительным целым числом"
                )

        if "status" in data:
            if data["status"] not in APPOINTMENT_STATUSES:
                raise AppointmentValidationError(
                    "Недопустимый статус записи"
                )

    def check_conflict(
        self,
        data: dict,
        exclude_id: int | None = None
    ) -> None:
        if data.get("status") == "отменён":
            return

        for appointment in self.repository.get_all():
            if appointment.id == exclude_id:
                continue

            if appointment.status == "отменён":
                continue

            if (
                appointment.doctor.casefold() == data["doctor"].casefold()
                and appointment.date == data["date"]
                and appointment.time == data["time"]
            ):
                raise AppointmentConflictError(
                    "У врача уже есть запись на указанное время"
                )

    def get_all(
        self,
        filters: dict | None = None,
        sort_by: str = "id",
        descending: bool = False
    ) -> list[Appointment]:
        appointments = self.repository.get_all()

        filters = filters or {}

        for field, value in filters.items():
            if field not in self.FIELDS:
                raise AppointmentValidationError(
                    f"Неизвестное поле фильтрации: {field}"
                )

            if value is None:
                continue

            appointments = [
                appointment
                for appointment in appointments
                if str(getattr(appointment, field)).casefold()
                == str(value).casefold()
            ]

        allowed_sort_fields = ("id",) + self.FIELDS

        if sort_by not in allowed_sort_fields:
            raise AppointmentValidationError(
                f"Недопустимое поле сортировки: {sort_by}"
            )

        return sorted(
            appointments,
            key=lambda item: getattr(item, sort_by),
            reverse=descending
        )

    def get_by_id(self, appointment_id: int) -> Appointment:
        return self.repository.get_by_id(appointment_id)

    def create(self, data: dict) -> Appointment:
        self.validate_data(data)

        clean_data = data.copy()

        for field in ("patient", "doctor", "specialty"):
            clean_data[field] = clean_data[field].strip()

        clean_data.setdefault("status", "запланирован")

        self.check_conflict(clean_data)

        return self.repository.create(clean_data)

    def update(
        self,
        appointment_id: int,
        data: dict,
        partial: bool = False
    ) -> Appointment:
        appointment = self.repository.get_by_id(appointment_id)

        self.validate_data(data, partial=partial)

        if partial:
            updated_data = appointment.to_dict()
            updated_data.update(data)
        else:
            updated_data = data.copy()
            updated_data.setdefault("status", "запланирован")

        for field in ("patient", "doctor", "specialty"):
            updated_data[field] = updated_data[field].strip()

        self.check_conflict(
            updated_data,
            exclude_id=appointment_id
        )

        return self.repository.update(appointment_id, updated_data)

    def delete(self, appointment_id: int) -> None:
        self.repository.delete(appointment_id)

    def search_by_patient(self, patient: str) -> list[Appointment]:
        if not patient.strip():
            raise AppointmentValidationError(
                "Имя пациента не может быть пустым"
            )

        return self.repository.find_by_patient(patient.strip())

    def get_by_doctor(self, doctor: str) -> list[Appointment]:
        return self.repository.find_by_doctor(doctor)

    def get_by_status(self, status: str) -> list[Appointment]:
        if status not in APPOINTMENT_STATUSES:
            raise AppointmentValidationError(
                "Недопустимый статус записи"
            )

        return self.repository.find_by_status(status)

    def get_available(self) -> list[Appointment]:
        return [
            appointment
            for appointment in self.repository.get_all()
            if appointment.status == "запланирован"
        ]

    def count_by_doctor(self, doctor: str) -> int:
        return self.repository.count_by_doctor(doctor)

    def paginate(
        self,
        appointments: list[Appointment],
        page: int = 1,
        limit: int = 10
    ) -> dict:
        if page < 1 or limit < 1 or limit > 100:
            raise AppointmentValidationError(
                "page должен быть >= 1, а limit — от 1 до 100"
            )

        total = len(appointments)
        start = (page - 1) * limit
        end = start + limit

        return {
            "items": [
                appointment.to_dict()
                for appointment in appointments[start:end]
            ],
            "page": page,
            "limit": limit,
            "total": total
        }
