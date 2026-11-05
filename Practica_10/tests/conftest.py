import pytest

from app import create_app
from app.repository import AppointmentRepository
from app.service import AppointmentService
from app.routes import repository as api_repository


@pytest.fixture
def repository():
    """Создание пустого хранилища для теста."""
    return AppointmentRepository()


@pytest.fixture
def service(repository):
    """Создание сервиса с тестовым хранилищем."""
    return AppointmentService(repository)


@pytest.fixture
def sample_appointment():
    """Пример корректных данных записи на приём."""
    return {
        "patient": "Иван Петров",
        "doctor": "Алексей Смирнов",
        "specialty": "Терапевт",
        "date": "2026-11-10",
        "time": "10:30",
        "room": 205,
        "status": "запланирован"
    }


@pytest.fixture
def app():
    """Создание Flask-приложения для тестирования."""
    api_repository.clear()

    application = create_app()
    application.config.update({
        "TESTING": True
    })

    yield application

    api_repository.clear()


@pytest.fixture
def client(app):
    """Тестовый HTTP-клиент Flask."""
    return app.test_client()


@pytest.fixture
def headers():
    """Заголовки для обращения к защищённому API."""
    return {
        "X-API-Key": "secret-key",
        "X-Client-Version": "1.0"
    }
