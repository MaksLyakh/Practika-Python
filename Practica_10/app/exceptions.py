class AppointmentError(Exception):
    """Базовое исключение для работы с записями."""

    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class AppointmentNotFoundError(AppointmentError):
    """Запись на приём не найдена."""

    status_code = 404

    def __init__(self, appointment_id: int):
        super().__init__(
            f"Запись на приём с ID {appointment_id} не найдена"
        )


class AppointmentValidationError(AppointmentError):
    """Некорректные данные записи."""

    status_code = 400


class AppointmentConflictError(AppointmentError):
    """Конфликт при создании или изменении записи."""

    status_code = 409


class UnauthorizedError(AppointmentError):
    """Отсутствует или неверен API-ключ."""

    status_code = 401

    def __init__(self):
        super().__init__("Неверный или отсутствующий API-ключ")
