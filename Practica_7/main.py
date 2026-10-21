
from repositories.memory_repository import MemoryClinicRepository
from infrastructure.notifier import ConsoleNotifier
from services.clinic_service import ClinicService
from ui.console import ConsoleUI


def main():
    repository = MemoryClinicRepository()
    notifier = ConsoleNotifier()

    clinic_service = ClinicService(repository, notifier)

    console = ConsoleUI(clinic_service)
    console.run()


if __name__ == "__main__":
    main()
