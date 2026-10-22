from models import Policy
from exceptions import PolicyNotFoundError, PolicyAlreadyExistsError


class PolicyRepository:
    def __init__(self):
        self.policies: dict[int, Policy] = {}

    def add(self, policy: Policy) -> None:
        if policy.id in self.policies:
            raise PolicyAlreadyExistsError(
                f"Полис с ID {policy.id} уже существует"
            )

        self.policies[policy.id] = policy

    def get(self, policy_id: int) -> Policy:
        if policy_id not in self.policies:
            raise PolicyNotFoundError(
                f"Полис с ID {policy_id} не найден"
            )

        return self.policies[policy_id]

    def get_all(self) -> list[Policy]:
        return list(self.policies.values())

    def update(self, policy: Policy) -> None:
        if policy.id not in self.policies:
            raise PolicyNotFoundError(
                f"Полис с ID {policy.id} не найден"
            )

        self.policies[policy.id] = policy

    def delete(self, policy_id: int) -> None:
        if policy_id not in self.policies:
            raise PolicyNotFoundError(
                f"Полис с ID {policy_id} не найден"
            )

        del self.policies[policy_id]

    def find_by_client(self, client_name: str) -> list[Policy]:
        return [
            policy
            for policy in self.policies.values()
            if client_name.lower() in policy.client_name.lower()
        ]
