class InsuranceError(Exception):
    """Базовое исключение системы страхования."""
    pass


class PolicyNotFoundError(InsuranceError):
    """Страховой полис не найден."""
    pass


class PolicyAlreadyExistsError(InsuranceError):
    """Полис с таким ID уже существует."""
    pass


class ValidationError(InsuranceError):
    """Некорректные данные страхового полиса."""
    pass


class ProtocolError(InsuranceError):
    """Ошибка формата запроса или сетевого протокола."""
    pass
