import pytest

import server
from repository import PolicyRepository
from service import InsuranceService


@pytest.fixture
def test_service(monkeypatch):
    """Создаёт отдельное хранилище для каждого теста."""
    repository = PolicyRepository()
    service = InsuranceService(repository)

    monkeypatch.setattr(server, "service", service)

    return service


@pytest.fixture
def sample_request():
    return {
        "command": "create_policy",
        "data": {
            "policy_id": 1,
            "client_name": "Иван Иванов",
            "insurance_type": "Авто",
            "amount": 500000,
            "duration_months": 12
        }
    }


def test_create_policy(test_service, sample_request):
    response = server.process_request(sample_request)

    assert response["status"] == "success"
    assert response["data"]["id"] == 1
    assert response["data"]["client_name"] == "Иван Иванов"


def test_get_policy(test_service, sample_request):
    server.process_request(sample_request)

    response = server.process_request({
        "command": "get_policy",
        "data": {"policy_id": 1}
    })

    assert response["status"] == "success"
    assert response["data"]["id"] == 1


def test_get_all_policies(test_service, sample_request):
    server.process_request(sample_request)

    response = server.process_request({
        "command": "get_all_policies",
        "data": {}
    })

    assert response["status"] == "success"
    assert len(response["data"]) == 1


def test_update_status(test_service, sample_request):
    server.process_request(sample_request)

    response = server.process_request({
        "command": "update_status",
        "data": {
            "policy_id": 1,
            "status": "Отменён"
        }
    })

    assert response["status"] == "success"
    assert response["data"]["status"] == "Отменён"


def test_delete_policy(test_service, sample_request):
    server.process_request(sample_request)

    response = server.process_request({
        "command": "delete_policy",
        "data": {"policy_id": 1}
    })

    assert response["status"] == "success"
    assert test_service.get_all_policies() == []


def test_find_by_client(test_service, sample_request):
    server.process_request(sample_request)

    response = server.process_request({
        "command": "find_by_client",
        "data": {"client_name": "Иван"}
    })

    assert response["status"] == "success"
    assert len(response["data"]) == 1


def test_calculate_cost(test_service, sample_request):
    server.process_request(sample_request)

    response = server.process_request({
        "command": "calculate_cost",
        "data": {"policy_id": 1}
    })

    assert response["status"] == "success"
    assert response["data"]["cost"] == 25000.0


def test_unknown_command(test_service):
    response = server.process_request({
        "command": "unknown_command",
        "data": {}
    })

    assert response["status"] == "error"
    assert "error" in response


def test_missing_field(test_service):
    response = server.process_request({
        "command": "get_policy",
        "data": {}
    })

    assert response["status"] == "error"
    assert "Отсутствует поле" in response["error"]


def test_invalid_data_format(test_service):
    response = server.process_request({
        "command": "get_policy",
        "data": [1, 2, 3]
    })

    assert response["status"] == "error"
    assert "error" in response


def test_nonexistent_policy(test_service):
    response = server.process_request({
        "command": "get_policy",
        "data": {"policy_id": 999}
    })

    assert response["status"] == "error"
    assert "не найден" in response["error"]


def test_duplicate_policy(test_service, sample_request):
    server.process_request(sample_request)

    response = server.process_request(sample_request)

    assert response["status"] == "error"
    assert "уже существует" in response["error"]
