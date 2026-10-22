from models import Policy, PolicyStatus
from repository import PolicyRepository
from exceptions import ValidationError


class InsuranceService:
    def __init__(self, repository: PolicyRepository):
        self.repository = repository

    def create_policy(
        self,
        policy_id: int,
        client_name: str,
        insurance_type: str,
        amount: float,
        duration_months: int
    ) -> dict:
        if type(policy_id) is not int or policy_id <= 0:
            raise ValidationError("ID полиса должен быть положительным целым числом")

        if not isinstance(client_name, str) or not client_name.strip():
            raise ValidationError("Имя клиента не может быть пустым")

        if not isinstance(insurance_type, str) or not insurance_type.strip():
            raise ValidationError("Тип страхования не может быть пустым")

        if type(amount) not in (int, float) or not 0 < amount < float("inf"):
            raise ValidationError("Страховая сумма должна быть положительным числом")

        if type(duration_months) is not int or duration_months <= 0:
            raise ValidationError("Срок страхования должен быть положительным целым числом")

        policy = Policy(
            id=policy_id,
            client_name=client_name.strip(),
            insurance_type=insurance_type.strip(),
            amount=amount,
            duration_months=duration_months
        )

        self.repository.add(policy)
        return policy.to_dict()

    def get_policy(self, policy_id: int) -> dict:
        policy = self.repository.get(policy_id)
        return policy.to_dict()

    def get_all_policies(self) -> list[dict]:
        return [
            policy.to_dict()
            for policy in self.repository.get_all()
        ]

    def update_status(self, policy_id: int, status: str) -> dict:
        policy = self.repository.get(policy_id)

        try:
            new_status = PolicyStatus(status)
        except (ValueError, TypeError):
            raise ValidationError("Недопустимый статус полиса")

        policy.status = new_status
        self.repository.update(policy)

        return policy.to_dict()

    def delete_policy(self, policy_id: int) -> dict:
        self.repository.delete(policy_id)
        return {"message": f"Полис {policy_id} удалён"}

    def find_by_client(self, client_name: str) -> list[dict]:
        if not isinstance(client_name, str) or not client_name.strip():
            raise ValidationError("Имя клиента не может быть пустым")

        policies = self.repository.find_by_client(client_name.strip())

        return [policy.to_dict() for policy in policies]

    def calculate_cost(self, policy_id: int) -> dict:
        """Рассчитывает стоимость страхования по полису."""
        policy = self.repository.get(policy_id)

        annual_rate = 0.05

        cost = round(
            policy.amount * annual_rate * policy.duration_months / 12,
            2
        )

        return {
            "policy_id": policy.id,
            "insurance_amount": policy.amount,
            "duration_months": policy.duration_months,
            "annual_rate": annual_rate,
            "cost": cost
        }
