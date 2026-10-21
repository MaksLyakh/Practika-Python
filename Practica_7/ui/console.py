
from interfaces.services import ClinicServiceInterface
from models.entities import Patient, Doctor


class ConsoleUI:

    def __init__(self, clinic_service: ClinicServiceInterface):
        self.clinic_service = clinic_service

    def show_menu(self):
        print("\n=== МЕДИЦИНСКАЯ КЛИНИКА ===")
        print("1. Добавить пациента")
        print("2. Добавить врача")
        print("3. Показать список врачей")
        print("4. Записать на приём")
        print("5. Завершить приём")
        print("6. Показать все приёмы")
        print("7. История посещений пациента")
        print("8. Получить результат приёма")
        print("0. Выход")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Выберите действие: ")

            try:
                if choice == "1":
                    patient_id = int(input("ID пациента: "))
                    name = input("ФИО пациента: ")

                    patient = Patient(patient_id, name)
                    self.clinic_service.register_patient(patient)

                elif choice == "2":
                    doctor_id = int(input("ID врача: "))
                    name = input("ФИО врача: ")
                    specialization = input("Специальность: ")

                    doctor = Doctor(
                        doctor_id,
                        name,
                        specialization
                    )
                    self.clinic_service.register_doctor(doctor)

                elif choice == "3":
                    doctors = self.clinic_service.get_doctors()

                    if not doctors:
                        print("Врачи пока не зарегистрированы")
                    else:
                        for doctor in doctors:
                            print(
                                f"{doctor.id}. {doctor.name} "
                                f"— {doctor.specialization}"
                            )

                elif choice == "4":
                    appointment_id = int(input("ID приёма: "))
                    patient_id = int(input("ID пациента: "))
                    doctor_id = int(input("ID врача: "))

                    self.clinic_service.create_appointment(
                        appointment_id,
                        patient_id,
                        doctor_id
                    )

                elif choice == "5":
                    appointment_id = int(input("ID приёма: "))
                    result = input("Результат приёма: ")
                    diagnosis_name = input("Диагноз: ")
                    diagnosis_description = input(
                        "Описание диагноза (необязательно): "
                    )

                    self.clinic_service.complete_appointment(
                        appointment_id,
                        result,
                        diagnosis_name,
                        diagnosis_description
                    )

                elif choice == "6":
                    appointments = self.clinic_service.get_appointments()

                    if not appointments:
                        print("Приёмов пока нет")
                    else:
                        for appointment in appointments:
                            self.show_appointment(appointment)

                elif choice == "7":
                    patient_id = int(input("ID пациента: "))

                    history = self.clinic_service.get_patient_history(
                        patient_id
                    )

                    if not history:
                        print("Завершённых посещений нет")
                    else:
                        for appointment in history:
                            self.show_appointment(appointment)

                elif choice == "8":
                    appointment_id = int(input("ID приёма: "))

                    result = self.clinic_service.get_result(
                        appointment_id
                    )
                    print(f"Результат приёма: {result}")

                elif choice == "0":
                    print("Завершение программы")
                    break

                else:
                    print("Неверный пункт меню")

            except ValueError as error:
                print(f"Ошибка: {error}")

    def show_appointment(self, appointment):
        print(f"\nПриём №{appointment.id}")
        print(f"Пациент ID: {appointment.patient_id}")
        print(f"Врач ID: {appointment.doctor_id}")
        print(f"Статус: {appointment.status.value}")
        print(f"Результат: {appointment.result or 'Нет'}")

        if appointment.diagnosis is not None:
            print(f"Диагноз: {appointment.diagnosis.name}")
            print(
                f"Описание: "
                f"{appointment.diagnosis.description or 'Нет'}"
            )
