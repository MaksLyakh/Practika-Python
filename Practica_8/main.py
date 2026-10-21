from repositories.memory_repository import MemoryAppointmentRepository
from factories.appointment_factory import AppointmentFactory
from observers.observers import AppointmentNotifier, ConsoleObserver
from services.clinic_service import ClinicService
from ui.console import ConsoleUI


def main():
    repository = MemoryAppointmentRepository()
    factory = AppointmentFactory()

    notifier = AppointmentNotifier()
    notifier.attach(ConsoleObserver())

    service = ClinicService(
        repository,
        factory,
        notifier
    )

    ui = ConsoleUI(service)
    ui.run()


if __name__ == "__main__":
    main()
