import pytest
import mongomock
import fakeredis
from app.repository import AppointmentRepository
from app.cache import ClinicCache
from app.service import ClinicService

@pytest.fixture
def repo():
    collection = mongomock.MongoClient()["clinic_lab13"]["appointment"]
    result = AppointmentRepository(collection)
    result.create_indexes()
    return result

@pytest.fixture
def redis_client():
    return fakeredis.FakeRedis(decode_responses=True)

@pytest.fixture
def cache(redis_client):
    return ClinicCache(redis_client, ttl=180)

@pytest.fixture
def service(repo, cache):
    return ClinicService(repo, cache)

@pytest.fixture
def sample():
    from app.models import make_appointment
    return make_appointment(
        "P01", "Тестовый пациент", "D01", "Тестовый врач",
        "Терапевт", "2026-12-10", "10:00",
        "ОРВИ", ["Общий анализ крови"], "scheduled", "TEST001"
    )
