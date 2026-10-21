class Clinic:
    def __init__(self):
        self.appointments = {}
        self.next_id = 1

    def create_appointment(self, patient, doctor, appointment_type, pricing_type):
        prices = {
            "1": 1500,
            "2": 2500,
            "3": 2000
        }

        types = {
            "1": "Терапевтический приём",
            "2": "Диагностическая процедура",
            "3": "Консультация"
        }

        if appointment_type not in types:
            print("Неверный тип приёма")
            return

        if pricing_type not in ("1", "2", "3"):
            print("Неверный тип стоимости")
            return

        price = prices[appointment_type]

        if pricing_type == "2":
            price *= 0.8
        elif pricing_type == "3":
            price *= 1.5

        appointment = {
            "id": self.next_id,
            "patient": patient,
            "doctor": doctor,
            "type": types[appointment_type],
            "price": price,
            "status": "Запланирован"
        }

        self.appointments[self.next_id] = appointment
        self.next_id += 1

        print("Запись успешно создана")
        print(f"Стоимость: {price:.2f} руб.")
        print("Уведомление: пациент записан на приём")

    def show_appointments(self):
        if not self.appointments:
            print("Записей пока нет")
            return

        for appointment in self.appointments.values():
            print(f"\nЗапись №{appointment['id']}")
            print(f"Пациент: {appointment['patient']}")
            print(f"Врач: {appointment['doctor']}")
            print(f"Тип: {appointment['type']}")
            print(f"Стоимость: {appointment['price']:.2f} руб.")
            print(f"Статус: {appointment['status']}")

    def complete_appointment(self, appointment_id):
        appointment = self.appointments.get(appointment_id)

        if appointment is None:
            print("Запись не найдена")
            return

        if appointment["status"] == "Завершён":
            print("Приём уже завершён")
            return

        appointment["status"] = "Завершён"
        print("Приём завершён")
        print("Уведомление: статус записи изменён")


def main():
    clinic = Clinic()

    while True:
        print("\n=== МЕДИЦИНСКАЯ КЛИНИКА ===")
        print("1. Создать запись")
        print("2. Показать записи")
        print("3. Завершить приём")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            patient = input("ФИО пациента: ").strip()
            doctor = input("ФИО врача: ").strip()

            if not patient or not doctor:
                print("ФИО пациента и врача не могут быть пустыми")
                continue

            print("\nТип приёма:")
            print("1. Терапевтический приём")
            print("2. Диагностическая процедура")
            print("3. Консультация")

            appointment_type = input("Выберите тип: ")

            print("\nТип стоимости:")
            print("1. Стандартная")
            print("2. Льготная")
            print("3. Срочная")

            pricing_type = input("Выберите стоимость: ")

            clinic.create_appointment(
                patient,
                doctor,
                appointment_type,
                pricing_type
            )

        elif choice == "2":
            clinic.show_appointments()

        elif choice == "3":
            try:
                appointment_id = int(input("ID записи: "))
                clinic.complete_appointment(appointment_id)
            except ValueError:
                print("Ошибка: введите целое число")

        elif choice == "0":
            print("Завершение программы")
            break

        else:
            print("Неверный пункт меню")


if __name__ == "__main__":
    main()
