from models.entities import Patient, Doctor
from models.enums import AppointmentType
from services.clinic_service import ClinicService
from strategies.pricing import (
    StandardPricing,
    DiscountPricing,
    UrgentPricing
)


class ConsoleUI:

    def __init__(self, service: ClinicService):
        self.service = service

    def create_appointment(self):
        patient_name = input("ФИО пациента: ").strip()
        doctor_name = input("ФИО врача: ").strip()

        if not patient_name or not doctor_name:
            print("ФИО не может быть пустым")
            return

        print("\nТип приёма:")
        print("1. Терапевтический приём")
        print("2. Диагностическая процедура")
        print("3. Консультация")

        appointment_types = {
            "1": AppointmentType.THERAPY,
            "2": AppointmentType.DIAGNOSTIC,
            "3": AppointmentType.CONSULTATION
        }

        type_choice = input("Выберите тип: ")

        if type_choice not in appointment_types:
            print("Неверный тип приёма")
            return

        print("\nТип стоимости:")
        print("1. Стандартная")
        print("2. Льготная")
        print("3. Срочная")

        strategies = {
            "1": StandardPricing(),
            "2": DiscountPricing(),
            "3": UrgentPricing()
        }

        price_choice = input("Выберите стоимость: ")

        if price_choice not in strategies:
            print("Неверный тип стоимости")
            return

        patient = Patient(1, patient_name)
        doctor = Doctor(1, doctor_name)

        appointment = self.service.create_appointment(
            patient,
            doctor,
            appointment_types[type_choice],
            strategies[price_choice]
        )

        print(f"Запись №{appointment.id} успешно создана")
        print(f"Стоимость: {appointment.price:.2f} руб.")

    def show_appointments(self):
        appointments = self.service.get_all_appointments()

        if not appointments:
            print("Записей пока нет")
            return

        for appointment in appointments:
            print(f"\nЗапись №{appointment.id}")
            print(f"Пациент: {appointment.patient.name}")
            print(f"Врач: {appointment.doctor.name}")
            print(f"Тип: {appointment.appointment_type.value}")
            print(f"Стоимость: {appointment.price:.2f} руб.")
            print(f"Статус: {appointment.status.value}")

    def complete_appointment(self):
        try:
            appointment_id = int(input("ID записи: "))
            self.service.complete_appointment(appointment_id)
            print("Приём завершён")
        except ValueError as error:
            print(f"Ошибка: {error}")

    def delete_appointment(self):
        try:
            appointment_id = int(input("ID записи: "))
            self.service.delete_appointment(appointment_id)
            print("Запись удалена")
        except ValueError as error:
            print(f"Ошибка: {error}")

    def run(self):
        while True:
            print("\n=== МЕДИЦИНСКАЯ КЛИНИКА ===")
            print("1. Создать запись")
            print("2. Показать записи")
            print("3. Завершить приём")
            print("4. Удалить запись")
            print("0. Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.create_appointment()
            elif choice == "2":
                self.show_appointments()
            elif choice == "3":
                self.complete_appointment()
            elif choice == "4":
                self.delete_appointment()
            elif choice == "0":
                print("Завершение программы")
                break
            else:
                print("Неверный пункт меню")
