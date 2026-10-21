# Первоначальная версия программы с нарушениями SOLID

class Clinic:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.appointments = {}

    def add_patient(self, patient_id, name):
        if patient_id in self.patients:
            print("Пациент уже существует")
            return

        self.patients[patient_id] = name
        print("Пациент добавлен")

    def add_doctor(self, doctor_id, name, specialization):
        if doctor_id in self.doctors:
            print("Врач уже существует")
            return

        self.doctors[doctor_id] = {
            "name": name,
            "specialization": specialization
        }
        print("Врач добавлен")

    def create_appointment(self, appointment_id, patient_id, doctor_id):
        if patient_id not in self.patients:
            print("Пациент не найден")
            return

        if doctor_id not in self.doctors:
            print("Врач не найден")
            return

        if appointment_id in self.appointments:
            print("Приём уже существует")
            return

        self.appointments[appointment_id] = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "status": "Запланирован",
            "result": ""
        }

        print("Приём создан")
        print("Уведомление: пациент записан к врачу")

    def complete_appointment(self, appointment_id, result):
        if appointment_id not in self.appointments:
            print("Приём не найден")
            return

        appointment = self.appointments[appointment_id]

        if appointment["status"] == "Завершён":
            print("Приём уже завершён")
            return

        appointment["status"] = "Завершён"
        appointment["result"] = result

        print("Приём завершён")
        print("Уведомление: результат приёма готов")

    def show_appointments(self):
        if not self.appointments:
            print("Приёмов нет")
            return

        for appointment_id, appointment in self.appointments.items():
            print(f"\nПриём №{appointment_id}")
            print(f"Пациент ID: {appointment['patient_id']}")
            print(f"Врач ID: {appointment['doctor_id']}")
            print(f"Статус: {appointment['status']}")
            print(f"Результат: {appointment['result']}")

    def show_result(self, appointment_id):
        if appointment_id not in self.appointments:
            print("Приём не найден")
            return

        appointment = self.appointments[appointment_id]

        if appointment["status"] != "Завершён":
            print("Приём ещё не завершён")
            return

        print("Результат приёма:", appointment["result"])


def main():
    clinic = Clinic()

    while True:
        print("\n=== МЕДИЦИНСКАЯ КЛИНИКА (ДО РЕФАКТОРИНГА) ===")
        print("1. Добавить пациента")
        print("2. Добавить врача")
        print("3. Записать на приём")
        print("4. Завершить приём")
        print("5. Показать приёмы")
        print("6. Получить результат приёма")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                patient_id = int(input("ID пациента: "))
                name = input("ФИО пациента: ")
                clinic.add_patient(patient_id, name)

            elif choice == "2":
                doctor_id = int(input("ID врача: "))
                name = input("ФИО врача: ")
                specialization = input("Специальность: ")
                clinic.add_doctor(doctor_id, name, specialization)

            elif choice == "3":
                appointment_id = int(input("ID приёма: "))
                patient_id = int(input("ID пациента: "))
                doctor_id = int(input("ID врача: "))

                clinic.create_appointment(
                    appointment_id,
                    patient_id,
                    doctor_id
                )

            elif choice == "4":
                appointment_id = int(input("ID приёма: "))
                result = input("Результат приёма: ")

                clinic.complete_appointment(appointment_id, result)

            elif choice == "5":
                clinic.show_appointments()

            elif choice == "6":
                appointment_id = int(input("ID приёма: "))
                clinic.show_result(appointment_id)

            elif choice == "0":
                print("Завершение программы")
                break

            else:
                print("Неверный пункт меню")

        except ValueError:
            print("Ошибка: необходимо ввести число")


if __name__ == "__main__":
    main()
