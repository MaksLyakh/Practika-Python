from models.entities import Patient, Doctor, Appointment
from models.enums import AppointmentType, AppointmentStatus
from interfaces.repository import AppointmentRepository
from interfaces.strategies import PricingStrategy
from factories.appointment_factory import AppointmentFactory
from observers.observers import AppointmentNotifier


class ClinicService:

    def __init__(
        self,
        repository: AppointmentRepository,
        factory: AppointmentFactory,
        notifier: AppointmentNotifier
    ):
        self.repository = repository
        self.factory = factory
        self.notifier = notifier
        self.next_id = 1

    def create_appointment(
        self,
        patient: Patient,
        doctor: Doctor,
        appointment_type: AppointmentType,
        pricing_strategy: PricingStrategy
    ) -> Appointment:

        appointment = self.factory.create_appointment(
            self.next_id,
            patient,
            doctor,
            appointment_type
        )

        appointment.price = pricing_strategy.calculate_price(
            appointment.price
        )

        self.repository.add(appointment)
        self.next_id += 1

        self.notifier.notify(
            f"Создана запись №{appointment.id} "
            f"для пациента {patient.name}"
        )

        return appointment

    def get_appointment(self, appointment_id: int) -> Appointment | None:
        return self.repository.get(appointment_id)

    def get_all_appointments(self) -> list[Appointment]:
        return self.repository.get_all()

    def complete_appointment(self, appointment_id: int) -> None:
        appointment = self.repository.get(appointment_id)

        if appointment is None:
            raise ValueError("Запись не найдена")

        if appointment.status == AppointmentStatus.COMPLETED:
            raise ValueError("Приём уже завершён")

        appointment.status = AppointmentStatus.COMPLETED

        self.notifier.notify(
            f"Приём №{appointment_id} завершён"
        )

    def delete_appointment(self, appointment_id: int) -> None:
        self.repository.delete(appointment_id)

        self.notifier.notify(
            f"Запись №{appointment_id} удалена"
        )
