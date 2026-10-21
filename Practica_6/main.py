import inspect

from models import Patient, Doctor, Appointment, AppointmentStatus, Person
from services import Clinic, ClinicError
from decorators import log_call, measure_time, repeat
from context import operation
from protocols import Reportable


# Безопасный ввод целого числа
def input_number(message: str) -> int:
    return int(input(message))


# Вывод информации через Protocol
def print_report(obj: Reportable) -> None:
    print(obj.get_report_data())


# Добавление объектов
def add_object(clinic: Clinic) -> None:
    print("\n1. Добавить пациента")
    print("2. Добавить врача")
    print("3. Добавить приём")

    choice = input("Выберите действие: ")

    if choice == "1":
        patient_id = input_number("ID пациента: ")
        name = input("ФИО пациента: ")
        age = input_number("Возраст: ")

        patient = Patient(patient_id, name, age)
        clinic.add_patient(patient)

        print("Пациент добавлен")

    elif choice == "2":
        doctor_id = input_number("ID врача: ")
        name = input("ФИО врача: ")
        specialization = input("Специальность: ")

        doctor = Doctor(doctor_id, name, specialization)
        clinic.add_doctor(doctor)

        print("Врач добавлен")

    elif choice == "3":
        appointment_id = input_number("ID приёма: ")
        patient_id = input_number("ID пациента: ")
        doctor_id = input_number("ID врача: ")
        duration = input_number("Продолжительность (мин): ")

        appointment = Appointment(
            appointment_id,
            patient_id,
            doctor_id,
            duration
        )

        clinic.add_appointment(appointment)

        print("Приём добавлен")

    else:
        print("Неверный пункт меню")


# Удаление объектов
def delete_object(clinic: Clinic) -> None:
    print("\n1. Удалить пациента")
    print("2. Удалить врача")
    print("3. Удалить приём")

    choice = input("Выберите действие: ")
    object_id = input_number("Введите ID: ")

    if choice == "1":
        clinic.delete_patient(object_id)
    elif choice == "2":
        clinic.delete_doctor(object_id)
    elif choice == "3":
        clinic.delete_appointment(object_id)
    else:
        print("Неверный пункт меню")
        return

    print("Объект удалён")


# Поиск объектов
def find_object(clinic: Clinic) -> None:
    print("\n1. Найти пациента")
    print("2. Найти врача")
    print("3. Найти приём")

    choice = input("Выберите действие: ")
    object_id = input_number("Введите ID: ")

    if choice == "1":
        obj = clinic.find_patient(object_id)
    elif choice == "2":
        obj = clinic.find_doctor(object_id)
    elif choice == "3":
        obj = clinic.find_appointment(object_id)
    else:
        print("Неверный пункт меню")
        return

    if obj is None:
        print("Объект не найден")
    else:
        print(obj)


# Вывод всех объектов
def show_objects(clinic: Clinic) -> None:
    print("\n=== ПАЦИЕНТЫ ===")

    if not clinic.patients:
        print("Пациентов нет")

    for patient in clinic.patients:
        print(patient)

    print("\n=== ВРАЧИ ===")

    if not clinic.doctors:
        print("Врачей нет")

    for doctor in clinic.doctors:
        print(doctor)

    print("\n=== ПРИЁМЫ ===")

    if not clinic.appointments:
        print("Приёмов нет")

    for appointment in clinic.appointments:
        print(
            f"ID: {appointment.id}, "
            f"Пациент: {appointment.patient_id}, "
            f"Врач: {appointment.doctor_id}, "
            f"Длительность: {appointment.duration} мин, "
            f"Статус: {appointment.status.value}"
        )


# Изменение статуса приёма
def change_appointment_status(clinic: Clinic) -> None:
    appointment_id = input_number("ID приёма: ")

    print("\n1. Запланирован")
    print("2. Подтверждён")
    print("3. Завершён")
    print("4. Отменён")

    choice = input("Новый статус: ")

    statuses = {
        "1": AppointmentStatus.PLANNED,
        "2": AppointmentStatus.CONFIRMED,
        "3": AppointmentStatus.COMPLETED,
        "4": AppointmentStatus.CANCELLED
    }

    if choice not in statuses:
        print("Неверный статус")
        return

    clinic.change_status(appointment_id, statuses[choice])

    print("Статус изменён")


# Операции предметной области
def special_operations(clinic: Clinic) -> None:
    print("\n1. Количество приёмов врача")
    print("2. Средняя продолжительность приёма")

    choice = input("Выберите действие: ")

    if choice == "1":
        doctor_id = input_number("ID врача: ")

        count = clinic.count_doctor_appointments(doctor_id)

        print(f"Количество приёмов врача: {count}")

    elif choice == "2":
        average = clinic.average_duration()

        print(f"Средняя продолжительность: {average:.2f} мин")

    else:
        print("Неверный пункт меню")


# Статистика
def show_statistics(clinic: Clinic) -> None:
    statistics = clinic.get_statistics()

    print("\n=== СТАТИСТИКА ===")

    for name, value in statistics.items():
        print(f"{name}: {value}")


# Интроспекция объекта
def inspect_object(clinic: Clinic) -> None:
    print("\n1. Пациент")
    print("2. Врач")
    print("3. Приём")

    choice = input("Выберите тип объекта: ")
    object_id = input_number("Введите ID: ")

    if choice == "1":
        obj = clinic.find_patient(object_id)
    elif choice == "2":
        obj = clinic.find_doctor(object_id)
    elif choice == "3":
        obj = clinic.find_appointment(object_id)
    else:
        print("Неверный пункт меню")
        return

    if obj is None:
        print("Объект не найден")
        return

    print("\n=== ИНТРОСПЕКЦИЯ ===")

    print("Тип объекта:", type(obj).__name__)
    print("Является Person:", isinstance(obj, Person))
    print("Класс наследуется от Person:",
          issubclass(type(obj), Person))

    print("Есть атрибут name:", hasattr(obj, "name"))

    if hasattr(obj, "name"):
        print("Значение name:", getattr(obj, "name"))

    print("\nАтрибуты и методы:")

    for name in dir(obj):
        if not name.startswith("_"):
            print(name)

    print("\nСигнатура конструктора:")
    print(inspect.signature(type(obj)))


# Демонстрация декораторов
@log_call
@measure_time
@repeat(3)
def demonstration() -> None:
    print("Выполняется демонстрационная функция")


def show_decorators() -> None:
    print("\n=== ДЕМОНСТРАЦИЯ ДЕКОРАТОРОВ ===")
    demonstration()


# Демонстрация контекстного менеджера
def show_context(clinic: Clinic) -> None:
    with operation("Получение статистики"):
        show_statistics(clinic)


# Демонстрация Protocol
def show_protocol(clinic: Clinic) -> None:
    print("\n=== ДЕМОНСТРАЦИЯ PROTOCOL ===")

    if clinic.patients:
        report: Reportable = clinic.patients[0]
        print_report(report)
    else:
        print("Нет пациентов для демонстрации")

    if clinic.doctors:
        report = clinic.doctors[0]
        print_report(report)
    else:
        print("Нет врачей для демонстрации")


# Главное меню
def main() -> None:
    clinic = Clinic()

    while True:
        print("\n========== МЕДИЦИНСКАЯ КЛИНИКА ==========")
        print("1. Добавить объект")
        print("2. Удалить объект")
        print("3. Найти объект")
        print("4. Вывести все объекты")
        print("5. Изменить статус приёма")
        print("6. Специальные операции")
        print("7. Статистика")
        print("8. Интроспекция")
        print("9. Демонстрация декораторов")
        print("10. Демонстрация контекстного менеджера")
        print("11. Демонстрация Protocol")
        print("0. Выход")

        choice = input("\nВыберите пункт: ")

        try:
            if choice == "1":
                add_object(clinic)
            elif choice == "2":
                delete_object(clinic)
            elif choice == "3":
                find_object(clinic)
            elif choice == "4":
                show_objects(clinic)
            elif choice == "5":
                change_appointment_status(clinic)
            elif choice == "6":
                special_operations(clinic)
            elif choice == "7":
                show_statistics(clinic)
            elif choice == "8":
                inspect_object(clinic)
            elif choice == "9":
                show_decorators()
            elif choice == "10":
                show_context(clinic)
            elif choice == "11":
                show_protocol(clinic)
            elif choice == "0":
                print("Завершение программы")
                break
            else:
                print("Неверный пункт меню")

        except ValueError:
            print("Ошибка: необходимо ввести число")

        except ClinicError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
