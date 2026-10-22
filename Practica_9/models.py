from dataclasses import dataclass
from enum import Enum


class PolicyStatus(Enum):
    ACTIVE = "Активен"
    EXPIRED = "Истёк"
    CANCELLED = "Отменён"


@dataclass
class Policy:
    id: int
    client_name: str
    insurance_type: str
    amount: float
    duration_months: int
    status: PolicyStatus = PolicyStatus.ACTIVE

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "client_name": self.client_name,
            "insurance_type": self.insurance_type,
            "amount": self.amount,
            "duration_months": self.duration_months,
            "status": self.status.value
        }
