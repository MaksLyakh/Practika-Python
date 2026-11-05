from typing import Any

from app.models import Appointment


def appointment_to_dict(appointment: Appointment) -> dict:
    """Преобразование записи на приём в словарь."""
    return appointment.to_dict()


def appointments_to_list(
    appointments: list[Appointment]
) -> list[dict]:
    """Преобразование списка записей в список словарей."""
    return [
        appointment_to_dict(appointment)
        for appointment in appointments
    ]


def success_response(
    data: Any = None,
    message: str = "Операция выполнена успешно"
) -> dict:
    """Формирование успешного ответа API."""
    response = {
        "success": True,
        "message": message
    }

    if data is not None:
        response["data"] = data

    return response


def error_response(
    message: str,
    status_code: int = 400
) -> dict:
    """Формирование ответа с ошибкой."""
    return {
        "success": False,
        "error": {
            "code": status_code,
            "message": message
        }
    }


def paginated_response(
    items: list[dict],
    page: int,
    limit: int,
    total: int
) -> dict:
    """Формирование ответа с пагинацией."""
    return {
        "success": True,
        "items": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    }
