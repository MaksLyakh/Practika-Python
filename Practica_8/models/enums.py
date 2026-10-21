from enum import Enum


class AppointmentType(Enum):
    THERAPY = "Терапевтический приём"
    DIAGNOSTIC = "Диагностическая процедура"
    CONSULTATION = "Консультация"


class AppointmentStatus(Enum):
    PLANNED = "Запланирован"
    COMPLETED = "Завершён"
