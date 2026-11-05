import json
import pytest
from app.models import make_appointment, validate_appointment
from app.seed import seed

def test_create_and_read(repo, sample):
    assert repo.create(sample) == "TEST001"
    assert repo.get("TEST001")["patient"]["name"] == "Тестовый пациент"

def test_missing(repo):
    assert repo.get("UNKNOWN") is None

def test_update(repo, sample):
    repo.create(sample)
    assert repo.update("TEST001", {"status": "completed"})["status"] == "completed"

def test_delete(repo, sample):
    repo.create(sample)
    assert repo.delete("TEST001") is True
    assert repo.delete("TEST001") is False

def test_filter(repo, sample):
    repo.create(sample)
    assert len(repo.list({"status": "scheduled"})) == 1
    assert len(repo.list({"status": "cancelled"})) == 0

def test_nested_filter(repo, sample):
    repo.create(sample)
    assert len(repo.list({"doctor.id": "D01"})) == 1

def test_array_filter(repo, sample):
    repo.create(sample)
    assert len(repo.list({"prescriptions": "Общий анализ крови"})) == 1

def test_aggregation(repo, sample):
    repo.create(sample)
    result = repo.ten_queries()
    assert len(result) == 10
    assert any(x["_id"] == "scheduled" for x in result["09_aggregation_by_status"])

def test_indexes(repo):
    names = set(repo.collection.index_information())
    assert {"unique_appointment_id", "doctor_schedule", "status_date"} <= names

def test_validation_invalid_status(sample):
    sample["status"] = "unknown"
    with pytest.raises(ValueError):
        validate_appointment(sample)

def test_validation_invalid_date(sample):
    sample["date"] = "2026-99-99"
    with pytest.raises(ValueError):
        validate_appointment(sample)

def test_redis_string_and_ttl(cache, redis_client):
    cache.set_json("test:json", {"x": 1})
    assert cache.get_json("test:json") == {"x": 1}
    assert 0 < redis_client.ttl("test:json") <= 180

def test_redis_hash(cache):
    assert cache.increment_doctor_views("D01") == 1
    assert cache.increment_doctor_views("D01") == 2
    assert cache.get_doctor_views("D01") == 2

def test_redis_sorted_set(cache, sample):
    cache.store_upcoming_ranking([sample])
    assert cache.earliest_ids() == ["TEST001"]

def test_cache_aside(service, sample):
    service.create_appointment(sample)
    first, source = service.get_appointment("TEST001", True)
    assert source == "MongoDB MISS"
    second, source = service.get_appointment("TEST001", True)
    assert source == "Redis HIT"
    assert first == second

def test_cache_invalidation(service, sample):
    service.create_appointment(sample)
    service.get_appointment("TEST001")
    service.update_appointment("TEST001", {"status": "completed"})
    item, source = service.get_appointment("TEST001", True)
    assert source == "MongoDB MISS"
    assert item["status"] == "completed"

def test_delete_invalidation(service, sample):
    service.create_appointment(sample)
    service.get_appointment("TEST001")
    assert service.delete_appointment("TEST001")
    assert service.get_appointment("TEST001") is None

def test_schedule_cache_invalidation(service, sample):
    service.create_appointment(sample)
    schedule, source = service.doctor_schedule("D01", "2026-12-10")
    assert source == "MongoDB MISS"
    _, source = service.doctor_schedule("D01", "2026-12-10")
    assert source == "Redis HIT"
    service.update_appointment("TEST001", {"time": "11:00"})
    schedule, source = service.doctor_schedule("D01", "2026-12-10")
    assert source == "MongoDB MISS"
    assert schedule[0]["time"] == "11:00"

def test_doctor_info_cache(service, sample):
    service.create_appointment(sample)
    _, source = service.doctor_info("D01")
    assert source == "MongoDB MISS"
    _, source = service.doctor_info("D01")
    assert source == "Redis HIT"
    assert service.cache.get_doctor_views("D01") == 2

def test_upcoming_cache(service, sample):
    service.create_appointment(sample)
    data, source = service.upcoming("2026-12-01")
    assert source == "MongoDB MISS"
    assert len(data) == 1
    _, source = service.upcoming("2026-12-01")
    assert source == "Redis HIT"
    service.update_appointment("TEST001", {"status": "cancelled"})
    data, source = service.upcoming("2026-12-01")
    assert source == "MongoDB MISS"
    assert data == []

def test_seed_24(repo, service):
    assert seed(repo, service) == 24
    assert seed(repo, service) == 0
    assert repo.collection.count_documents({}) == 24

def test_no_short_ttl(redis_client):
    from app.cache import ClinicCache
    with pytest.raises(ValueError):
        ClinicCache(redis_client, ttl=29)

def test_invalid_update(repo, sample):
    repo.create(sample)
    with pytest.raises(ValueError):
        repo.update("TEST001", {"appointment_id": "HACK"})
    assert repo.get("TEST001") is not None
