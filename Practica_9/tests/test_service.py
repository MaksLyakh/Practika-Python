import pytest

from repository import PolicyRepository
from service import InsuranceService
from exceptions import (
    ValidationError,
    PolicyNotFoundError,
    PolicyAlreadyExistsError
)


@pytest.fixture
def service():
    repository = PolicyRepository()
    return InsuranceService(repository)


@pytest.fixture
def sample_data():
    return {
        "policy_id": 1,
        "client_name": "Иван Иванов",
        "insurance_type": "Авто",
        "amount": 500000,
        "duration_months": 12
    }


def test_create_policy(service, sample_data):
    policy = service.create_policy(**sample_data)

    assert policy["id"] == 1
    assert policy["client_name"] == "Иван Иванов"
    assert policy["status"] == "Активен"


def test_create_duplicate_policy(service, sample_data):
    service.create_policy(**sample_data)

    with pytest.raises(PolicyAlreadyExistsError):
        service.create_policy(**sample_data)


def test_invalid_policy_id(service, sample_data):
    sample_data["policy_id"] = -1

    with pytest.raises(ValidationError):
        service.create_policy(**sample_data)


def test_empty_client_name(service, sample_data):
    sample_data["client_name"] = "   "

    with pytest.raises(ValidationError):
        service.create_policy(**sample_data)


def test_empty_insurance_type(service, sample_data):
    sample_data["insurance_type"] = ""

    with pytest.raises(ValidationError):
        service.create_policy(**sample_data)


def test_negative_amount(service, sample_data):
    sample_data["amount"] = -1000

    with pytest.raises(ValidationError):
        service.create_policy(**sample_data)


def test_invalid_duration(service, sample_data):
    sample_data["duration_months"] = 0

    with pytest.raises(ValidationError):
        service.create_policy(**sample_data)


def test_get_policy(service, sample_data):
    service.create_policy(**sample_data)

    policy = service.get_policy(1)

    assert policy["id"] == 1
    assert policy["amount"] == 500000


def test_get_nonexistent_policy(service):
    with pytest.raises(PolicyNotFoundError):
        service.get_policy(999)


def test_get_all_policies(service, sample_data):
    service.create_policy(**sample_data)

    policies = service.get_all_policies()

    assert len(policies) == 1
    assert policies[0]["id"] == 1


def test_update_status(service, sample_data):
    service.create_policy(**sample_data)

    policy = service.update_status(1, "Отменён")

    assert policy["status"] == "Отменён"


def test_invalid_status(service, sample_data):
    service.create_policy(**sample_data)

    with pytest.raises(ValidationError):
        service.update_status(1, "Неизвестный")


def test_delete_policy(service, sample_data):
    service.create_policy(**sample_data)

    result = service.delete_policy(1)

    assert result["message"] == "Полис 1 удалён"
    assert service.get_all_policies() == []


def test_find_by_client(service, sample_data):
    service.create_policy(**sample_data)

    policies = service.find_by_client("иван")

    assert len(policies) == 1
    assert policies[0]["client_name"] == "Иван Иванов"


def test_find_by_client_empty_name(service):
    with pytest.raises(ValidationError):
        service.find_by_client("   ")


def test_calculate_cost(service, sample_data):
    service.create_policy(**sample_data)

    result = service.calculate_cost(1)

    assert result["policy_id"] == 1
    assert result["insurance_amount"] == 500000
    assert result["duration_months"] == 12
    assert result["annual_rate"] == 0.05
    assert result["cost"] == 25000.0


def test_calculate_cost_six_months(service, sample_data):
    sample_data["duration_months"] = 6
    service.create_policy(**sample_data)

    result = service.calculate_cost(1)

    assert result["cost"] == 12500.0


def test_calculate_cost_two_years(service, sample_data):
    sample_data["duration_months"] = 24
    service.create_policy(**sample_data)

    result = service.calculate_cost(1)

    assert result["cost"] == 50000.0


def test_calculate_cost_nonexistent_policy(service):
    with pytest.raises(PolicyNotFoundError):
        service.calculate_cost(999)


def test_calculate_cost_rounding(service, sample_data):
    sample_data["amount"] = 12345
    sample_data["duration_months"] = 7

    service.create_policy(**sample_data)

    result = service.calculate_cost(1)

    assert result["cost"] == 360.06
