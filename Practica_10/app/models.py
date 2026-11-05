from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Appointment:
    id: int
    patient: str
    doctor: str
    specialty: str
    date: str
    time: str
    room: int
    status: str = "запланирован"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Appointment":
        return cls(
            id=data["id"],
            patient=data["patient"],
            doctor=data["doctor"],
            specialty=data["specialty"],
            date=data["date"],
            time=data["time"],
            room=data["room"],
            status=data.get("status", "запланирован")
        )


APPOINTMENT_STATUSES = (
    "запланирован",
    "подтверждён",
    "завершён",
    "отменён"
)
