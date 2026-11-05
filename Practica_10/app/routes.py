import hashlib
import json

from flask import Blueprint, jsonify, request, make_response

from app.repository import AppointmentRepository
from app.service import AppointmentService
from app.schemas import (
    appointment_to_dict,
    appointments_to_list,
    success_response,
    error_response
)
from app.exceptions import (
    AppointmentError,
    AppointmentValidationError
)


appointments_bp = Blueprint("appointments", __name__)

repository = AppointmentRepository()
service = AppointmentService(repository)


def get_json_data() -> dict:
    """Получение JSON из тела запроса."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        raise AppointmentValidationError(
            "Тело запроса должно содержать JSON-объект"
        )

    return data


def get_positive_int(name: str, default: int) -> int:
    """Чтение положительного целого параметра."""
    value = request.args.get(name, str(default))

    try:
        number = int(value)
    except (ValueError, TypeError):
        raise AppointmentValidationError(
            f"Параметр '{name}' должен быть целым числом"
        )

    if number < 1:
        raise AppointmentValidationError(
            f"Параметр '{name}' должен быть больше нуля"
        )

    return number


def make_etag(data: dict) -> str:
    """Создание ETag на основе содержимого записи."""
    content = json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True
    )

    digest = hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

    return f'"{digest}"'


def appointment_response(appointment, status_code: int = 200):
    """Ответ с поддержкой ETag."""
    data = appointment_to_dict(appointment)
    etag = make_etag(data)

    if (
        request.method == "GET"
        and request.headers.get("If-None-Match") == etag
    ):
        response = make_response("", 304)
        response.headers["ETag"] = etag
        return response

    response = make_response(
        jsonify(success_response(
            data,
            "Запись получена"
            if status_code == 200
            else "Запись успешно создана"
        )),
        status_code
    )

    response.headers["ETag"] = etag
    return response


@appointments_bp.route("/appointments", methods=["GET"])
def get_appointments():
    """Получение списка записей с фильтрацией и пагинацией."""
    page = get_positive_int("page", 1)
    limit = get_positive_int("limit", 10)

    if limit > 100:
        raise AppointmentValidationError(
            "Параметр 'limit' не должен превышать 100"
        )

    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc").lower()

    if order not in ("asc", "desc"):
        raise AppointmentValidationError(
            "Параметр 'order' должен быть asc или desc"
        )

    filter_fields = (
        "patient",
        "doctor",
        "specialty",
        "date",
        "time",
        "room",
        "status"
    )

    filters = {
        field: request.args.get(field)
        for field in filter_fields
        if request.args.get(field) is not None
    }

    appointments = service.get_all(
        filters=filters,
        sort_by=sort_by,
        descending=(order == "desc")
    )

    result = service.paginate(
        appointments,
        page=page,
        limit=limit
    )

    return jsonify(result), 200


@appointments_bp.route("/appointments/<int:appointment_id>", methods=["GET"])
def get_appointment(appointment_id: int):
    """Получение записи по ID."""
    appointment = service.get_by_id(appointment_id)

    return appointment_response(appointment)


@appointments_bp.route("/appointments", methods=["POST"])
def create_appointment():
    """Создание новой записи."""
    data = get_json_data()

    appointment = service.create(data)

    response = appointment_response(
        appointment,
        status_code=201
    )

    response.headers["Location"] = (
        f"/appointments/{appointment.id}"
    )

    return response


@appointments_bp.route(
    "/appointments/<int:appointment_id>",
    methods=["PUT"]
)
def update_appointment(appointment_id: int):
    """Полное обновление записи."""
    data = get_json_data()

    appointment = service.update(
        appointment_id,
        data,
        partial=False
    )

    return jsonify(success_response(
        appointment_to_dict(appointment),
        "Запись полностью обновлена"
    )), 200


@appointments_bp.route(
    "/appointments/<int:appointment_id>",
    methods=["PATCH"]
)
def patch_appointment(appointment_id: int):
    """Частичное обновление записи."""
    data = get_json_data()

    appointment = service.update(
        appointment_id,
        data,
        partial=True
    )

    return jsonify(success_response(
        appointment_to_dict(appointment),
        "Запись частично обновлена"
    )), 200


@appointments_bp.route(
    "/appointments/<int:appointment_id>",
    methods=["DELETE"]
)
def delete_appointment(appointment_id: int):
    """Удаление записи."""
    service.delete(appointment_id)

    return jsonify(success_response(
        message="Запись успешно удалена"
    )), 200


@appointments_bp.route("/appointments/search", methods=["GET"])
def search_appointments():
    """Поиск записей по имени пациента."""
    patient = request.args.get("patient", "")

    appointments = service.search_by_patient(patient)

    return jsonify(success_response(
        appointments_to_list(appointments),
        "Результаты поиска"
    )), 200


@appointments_bp.route("/appointments/available", methods=["GET"])
def get_available_appointments():
    """Получение запланированных приёмов."""
    appointments = service.get_available()

    return jsonify(success_response(
        appointments_to_list(appointments),
        "Список запланированных приёмов"
    )), 200


@appointments_bp.route("/appointments/stats", methods=["GET"])
def get_statistics():
    """Статистика записей по статусам."""
    appointments = repository.get_all()

    statistics = {
        "total": len(appointments),
        "planned": sum(
            a.status == "запланирован"
            for a in appointments
        ),
        "confirmed": sum(
            a.status == "подтверждён"
            for a in appointments
        ),
        "completed": sum(
            a.status == "завершён"
            for a in appointments
        ),
        "cancelled": sum(
            a.status == "отменён"
            for a in appointments
        )
    }

    return jsonify(success_response(
        statistics,
        "Статистика записей"
    )), 200


@appointments_bp.route(
    "/appointments/doctor/<string:doctor>",
    methods=["GET"]
)
def get_doctor_appointments(doctor: str):
    """Получение записей конкретного врача."""
    appointments = service.get_by_doctor(doctor)

    return jsonify(success_response(
        appointments_to_list(appointments),
        "Записи выбранного врача"
    )), 200


@appointments_bp.errorhandler(AppointmentError)
def handle_appointment_error(error: AppointmentError):
    """Обработка ошибок приложения."""
    return jsonify(error_response(
        error.message,
        error.status_code
    )), error.status_code


@appointments_bp.errorhandler(404)
def handle_not_found(error):
    """Обработка неизвестного маршрута внутри Blueprint."""
    return jsonify(error_response(
        "Ресурс не найден",
        404
    )), 404


@appointments_bp.errorhandler(405)
def handle_method_not_allowed(error):
    """Обработка неподдерживаемого HTTP-метода."""
    return jsonify(error_response(
        "HTTP-метод не поддерживается",
        405
    )), 405
