import unittest

from models.entities import Patient, Doctor
from models.enums import AppointmentType, AppointmentStatus
from factories.appointment_factory import AppointmentFactory
from repositories.memory_repository import MemoryAppointmentRepository
from strategies.pricing import (
    StandardPricing,
    DiscountPricing,
    UrgentPricing
)
from observers.observers import AppointmentNotifier
from services.clinic_service import ClinicService


class TestClinic(unittest.TestCase):

    def setUp(self):
        self.repository = MemoryAppointmentRepository()
        self.factory = AppointmentFactory()
        self.notifier = AppointmentNotifier()

        self.service = ClinicService(
            self.repository,
            self.factory,
            self.notifier
        )

        self.patient = Patient(1, "Иван Иванов")
        self.doctor = Doctor(1, "Пётр Петров")

    def create_appointment(self, appointment_type=AppointmentType.THERAPY):
        return self.service.create_appointment(
            self.patient,
            self.doctor,
            appointment_type,
            StandardPricing()
        )

    def test_factory_therapy(self):
        appointment = self.create_appointment()
        self.assertEqual(appointment.price, 1500)

    def test_factory_diagnostic(self):
        appointment = self.create_appointment(
            AppointmentType.DIAGNOSTIC
        )
        self.assertEqual(appointment.price, 2500)

    def test_factory_consultation(self):
        appointment = self.create_appointment(
            AppointmentType.CONSULTATION
        )
        self.assertEqual(appointment.price, 2000)

    def test_standard_pricing(self):
        strategy = StandardPricing()
        self.assertEqual(strategy.calculate_price(1500), 1500)

    def test_discount_pricing(self):
        strategy = DiscountPricing()
        self.assertEqual(strategy.calculate_price(1500), 1200)

    def test_urgent_pricing(self):
        strategy = UrgentPricing()
        self.assertEqual(strategy.calculate_price(1500), 2250)

    def test_repository(self):
        appointment = self.create_appointment()

        result = self.repository.get(appointment.id)

        self.assertEqual(result, appointment)

    def test_complete_appointment(self):
        appointment = self.create_appointment()

        self.service.complete_appointment(appointment.id)

        self.assertEqual(
            appointment.status,
            AppointmentStatus.COMPLETED
        )

    def test_delete_appointment(self):
        appointment = self.create_appointment()

        self.service.delete_appointment(appointment.id)

        self.assertIsNone(
            self.repository.get(appointment.id)
        )

    def test_observer(self):
        messages = []

        class TestObserver:
            def update(self, message):
                messages.append(message)

        self.notifier.attach(TestObserver())

        self.create_appointment()

        self.assertEqual(len(messages), 1)
        self.assertIn("Создана запись", messages[0])


if __name__ == "__main__":
    unittest.main()
