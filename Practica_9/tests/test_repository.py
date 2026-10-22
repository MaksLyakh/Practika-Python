import pytest

from models import Policy, PolicyStatus
from repository import PolicyRepository
from exceptions import (
    PolicyNotFoundError,
    PolicyAlreadyExistsError
)


@pytest.fixture
def repository():
    return PolicyRepository()


@pytest.fixture
def sample_policy():
    return Policy(
        id=1,
        client_name="Иван Иванов",
        insurance_type="Авто",
        amount=500000,
        duration_months=12
    )


def test_add_policy(repository, sample_policy):
    repository.add(sample_policy)

    assert repository.get(1) == sample_policy


def test_add_duplicate_policy(repository, sample_policy):
    repository.add(sample_policy)

    with pytest.raises(PolicyAlreadyExistsError):
        repository.add(sample_policy)


def test_get_nonexistent_policy(repository):
    with pytest.raises(PolicyNotFoundError):
        repository.get(999)


def test_get_all_policies(repository, sample_policy):
    repository.add(sample_policy)

    policies = repository.get_all()

    assert len(policies) == 1
    assert policies[0].client_name == "Иван Иванов"


def test_update_policy(repository, sample_policy):
    repository.add(sample_policy)

    updated_policy = Policy(
        id=1,
        client_name="Иван Иванов",
        insurance_type="Авто",
        amount=750000,
        duration_months=24,
        status=PolicyStatus.ACTIVE
    )

    repository.update(updated_policy)

    assert repository.get(1).amount == 750000
    assert repository.get(1).duration_months == 24


def test_update_nonexistent_policy(repository, sample_policy):
    with pytest.raises(PolicyNotFoundError):
        repository.update(sample_policy)


def test_delete_policy(repository, sample_policy):
    repository.add(sample_policy)
    repository.delete(1)

    assert repository.get_all() == []


def test_delete_nonexistent_policy(repository):
    with pytest.raises(PolicyNotFoundError):
        repository.delete(999)


def test_find_by_client(repository, sample_policy):
    repository.add(sample_policy)

    results = repository.find_by_client("иван")

    assert len(results) == 1
    assert results[0].id == 1


def test_find_by_client_no_results(repository):
    results = repository.find_by_client("Пётр")

    assert results == []
