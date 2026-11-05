import pytest

from app.exceptions import (
    AppointmentValidationError,
    AppointmentConflictError,
    AppointmentNotFoundError
)


def test_create_appointment(service, sample_appointment):
    """Создание записи с корректными данными."""
    appointment = service.create(sample_appointment)

    assert appointment.id == 1
    assert appointment.patient == "Иван Петров"
    assert appointment.status == "запланирован"


def test_create_without_required_field(service, sample_appointment):
    """Проверка отсутствующего обязательного поля."""
    data = sample_appointment.copy()
    del data["patient"]

    with pytest.raises(AppointmentValidationError):
        service.create(data)


def test_create_with_empty_patient(service, sample_appointment):
    """Проверка пустого имени пациента."""
    data = sample_appointment.copy()
    data["patient"] = ""

    with pytest.raises(AppointmentValidationError):
        service.create(data)


def test_create_with_invalid_date(service, sample_appointment):
    """Проверка некорректной даты."""
    data = sample_appointment.copy()
    data["date"] = "2026-15-40"

    with pytest.raises(AppointmentValidationError):
        service.create(data)


def test_create_with_invalid_time(service, sample_appointment):
    """Проверка некорректного времени."""
    data = sample_appointment.copy()
    data["time"] = "28:90"

    with pytest.raises(AppointmentValidationError):
        service.create(data)


def test_create_with_invalid_room(service, sample_appointment):
    """Проверка некорректного номера кабинета."""
    data = sample_appointment.copy()
    data["room"] = -5

    with pytest.raises(AppointmentValidationError):
        service.create(data)


def test_create_with_invalid_status(service, sample_appointment):
    """Проверка недопустимого статуса."""
    data = sample_appointment.copy()
    data["status"] = "неизвестный"

    with pytest.raises(AppointmentValidationError):
        service.create(data)


def test_create_with_unknown_field(service, sample_appointment):
    """Проверка неизвестного поля."""
    data = sample_appointment.copy()
    data["extra_field"] = "test"

    with pytest.raises(AppointmentValidationError):
        service.create(data)


def test_appointment_conflict(service, sample_appointment):
    """Проверка двойной записи к одному врачу."""
    service.create(sample_appointment)

    data = sample_appointment.copy()
    data["patient"] = "Мария Иванова"

    with pytest.raises(AppointmentConflictError):
        service.create(data)


def test_different_time_no_conflict(service, sample_appointment):
    """Разное время приёма не вызывает конфликт."""
    service.create(sample_appointment)

    data = sample_appointment.copy()
    data["time"] = "11:30"

    second = service.create(data)

    assert second.id == 2


def test_cancelled_appointment_no_conflict(service, sample_appointment):
    """Отменённая запись не блокирует время врача."""
    data = sample_appointment.copy()
    data["status"] = "отменён"

    service.create(data)

    second = service.create(sample_appointment)

    assert second.id == 2


def test_get_by_id(service, sample_appointment):
    """Получение записи по ID."""
    created = service.create(sample_appointment)

    result = service.get_by_id(created.id)

    assert result.patient == "Иван Петров"


def test_get_nonexistent_appointment(service):
    """Получение отсутствующей записи."""
    with pytest.raises(AppointmentNotFoundError):
        service.get_by_id(999)


def test_full_update(service, sample_appointment):
    """Полное обновление записи."""
    created = service.create(sample_appointment)

    data = sample_appointment.copy()
    data["patient"] = "Мария Иванова"
    data["time"] = "12:00"

    updated = service.update(
        created.id,
        data,
        partial=False
    )

    assert updated.patient == "Мария Иванова"
    assert updated.time == "12:00"


def test_partial_update(service, sample_appointment):
    """Частичное обновление записи."""
    created = service.create(sample_appointment)

    updated = service.update(
        created.id,
        {"status": "подтверждён"},
        partial=True
    )

    assert updated.status == "подтверждён"
    assert updated.patient == "Иван Петров"


def test_delete_appointment(service, sample_appointment):
    """Удаление записи."""
    created = service.create(sample_appointment)

    service.delete(created.id)

    assert service.get_all() == []


def test_filter_by_status(service, sample_appointment):
    """Фильтрация записей по статусу."""
    service.create(sample_appointment)

    data = sample_appointment.copy()
    data["patient"] = "Мария Иванова"
    data["time"] = "11:30"
    data["status"] = "подтверждён"

    service.create(data)

    result = service.get_all(
        filters={"status": "подтверждён"}
    )

    assert len(result) == 1
    assert result[0].patient == "Мария Иванова"


def test_sort_by_time(service, sample_appointment):
    """Сортировка записей по времени."""
    data1 = sample_appointment.copy()
    data1["time"] = "14:00"

    data2 = sample_appointment.copy()
    data2["time"] = "09:00"

    service.create(data1)
    service.create(data2)

    result = service.get_all(sort_by="time")

    assert result[0].time == "09:00"
    assert result[1].time == "14:00"


def test_search_by_patient(service, sample_appointment):
    """Поиск пациента по части имени."""
    service.create(sample_appointment)

    result = service.search_by_patient("Иван")

    assert len(result) == 1
    assert result[0].patient == "Иван Петров"


def test_get_available(service, sample_appointment):
    """Получение запланированных приёмов."""
    service.create(sample_appointment)

    data = sample_appointment.copy()
    data["status"] = "отменён"

    service.create(data)

    result = service.get_available()

    assert len(result) == 1
    assert result[0].status == "запланирован"


def test_pagination(service, sample_appointment):
    """Проверка пагинации."""
    for index in range(5):
        data = sample_appointment.copy()
        data["time"] = f"{10 + index:02d}:00"

        service.create(data)

    appointments = service.get_all()

    result = service.paginate(
        appointments,
        page=2,
        limit=2
    )

    assert result["page"] == 2
    assert result["limit"] == 2
    assert result["total"] == 5
    assert len(result["items"]) == 2
    assert result["items"][0]["id"] == 3


def test_invalid_pagination(service):
    """Проверка некорректных параметров пагинации."""
    with pytest.raises(AppointmentValidationError):
        service.paginate([], page=0, limit=10)


def test_invalid_sort_field(service):
    """Проверка неизвестного поля сортировки."""
    with pytest.raises(AppointmentValidationError):
        service.get_all(sort_by="unknown")
