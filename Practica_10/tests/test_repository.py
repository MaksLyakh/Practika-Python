import pytest

from app.exceptions import AppointmentNotFoundError


def test_create_appointment(repository, sample_appointment):
    """Проверка создания записи."""
    appointment = repository.create(sample_appointment)

    assert appointment.id == 1
    assert appointment.patient == "Иван Петров"
    assert appointment.doctor == "Алексей Смирнов"
    assert appointment.room == 205


def test_get_all_appointments(repository, sample_appointment):
    """Проверка получения всех записей."""
    repository.create(sample_appointment)

    second_appointment = sample_appointment.copy()
    second_appointment["patient"] = "Мария Иванова"

    repository.create(second_appointment)

    appointments = repository.get_all()

    assert len(appointments) == 2


def test_get_appointment_by_id(repository, sample_appointment):
    """Проверка получения записи по ID."""
    created = repository.create(sample_appointment)

    appointment = repository.get_by_id(created.id)

    assert appointment.id == created.id
    assert appointment.patient == "Иван Петров"


def test_get_nonexistent_appointment(repository):
    """Проверка ошибки при поиске отсутствующей записи."""
    with pytest.raises(AppointmentNotFoundError):
        repository.get_by_id(999)


def test_update_appointment(repository, sample_appointment):
    """Проверка изменения записи."""
    created = repository.create(sample_appointment)

    updated = repository.update(
        created.id,
        {"status": "подтверждён"}
    )

    assert updated.status == "подтверждён"
    assert updated.patient == "Иван Петров"


def test_delete_appointment(repository, sample_appointment):
    """Проверка удаления записи."""
    created = repository.create(sample_appointment)

    repository.delete(created.id)

    assert len(repository.get_all()) == 0

    with pytest.raises(AppointmentNotFoundError):
        repository.get_by_id(created.id)


def test_find_by_doctor(repository, sample_appointment):
    """Проверка поиска записей по врачу."""
    repository.create(sample_appointment)

    second_appointment = sample_appointment.copy()
    second_appointment["doctor"] = "Ольга Соколова"

    repository.create(second_appointment)

    result = repository.find_by_doctor("Алексей Смирнов")

    assert len(result) == 1
    assert result[0].patient == "Иван Петров"


def test_find_by_status(repository, sample_appointment):
    """Проверка поиска записей по статусу."""
    repository.create(sample_appointment)

    second_appointment = sample_appointment.copy()
    second_appointment["status"] = "отменён"

    repository.create(second_appointment)

    result = repository.find_by_status("отменён")

    assert len(result) == 1
    assert result[0].status == "отменён"


def test_find_by_date(repository, sample_appointment):
    """Проверка поиска записей по дате."""
    repository.create(sample_appointment)

    result = repository.find_by_date("2026-11-10")

    assert len(result) == 1
    assert result[0].date == "2026-11-10"


def test_find_by_patient(repository, sample_appointment):
    """Проверка поиска пациента по части имени."""
    repository.create(sample_appointment)

    result = repository.find_by_patient("Иван")

    assert len(result) == 1
    assert result[0].patient == "Иван Петров"


def test_count_by_doctor(repository, sample_appointment):
    """Проверка подсчёта записей врача."""
    repository.create(sample_appointment)

    second_appointment = sample_appointment.copy()
    second_appointment["patient"] = "Мария Иванова"

    repository.create(second_appointment)

    count = repository.count_by_doctor("Алексей Смирнов")

    assert count == 2


def test_clear_repository(repository, sample_appointment):
    """Проверка очистки хранилища."""
    repository.create(sample_appointment)

    repository.clear()

    assert repository.get_all() == []

    new_appointment = repository.create(sample_appointment)

    assert new_appointment.id == 1
