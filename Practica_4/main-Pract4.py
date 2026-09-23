from models import Computer
from services import ComputerService
from storage import load_json, save_json, export_csv
from exceptions import ComputerNotFoundError


def input_ram():
    while True:
        try:
            ram = int(input("Введите объём RAM (ГБ): "))

            if ram <= 0:
                print("RAM должна быть больше 0.")
            else:
                return ram

        except ValueError:
            print("Ошибка: необходимо ввести целое число.")


def input_price():
    while True:
        try:
            price = float(input("Введите цену: "))

            if price <= 0:
                print("Цена должна быть больше 0.")
            else:
                return price

        except ValueError:
            print("Ошибка: необходимо ввести число.")


def create_computer(service):
    name = input("Введите название компьютера: ")
    processor = input("Введите процессор: ")
    ram = input_ram()
    storage = input("Введите накопитель: ")
    price = input_price()

    computer = Computer(
        name,
        processor,
        ram,
        storage,
        price
    )

    service.add_computer(computer)

    print("Компьютер добавлен.")


def change_computer(service):
    name = input("Введите название компьютера: ")

    try:
        computer = service.find_computer(name)

        print("Текущие данные:")
        print(computer)

        processor = input("Введите новый процессор: ")
        ram = input_ram()
        storage = input("Введите новый накопитель: ")
        price = input_price()

        service.change_computer(
            name,
            processor,
            ram,
            storage,
            price
        )

        print("Данные компьютера изменены.")

    except ComputerNotFoundError as error:
        print(error)


def find_computer(service):
    name = input("Введите название компьютера: ")

    try:
        computer = service.find_computer(name)
        print(computer)

    except ComputerNotFoundError as error:
        print(error)


def filter_computers(service):
    min_ram = input_ram()

    computers = service.filter_by_ram(min_ram)

    if len(computers) == 0:
        print("Подходящие компьютеры не найдены.")
        return

    for computer in computers:
        print(computer)


def show_sorted_computers(service):
    computers = service.sort_by_price()

    if len(computers) == 0:
        print("Каталог компьютеров пуст.")
        return

    for computer in computers:
        print(computer)


def main():
    computers = load_json()
    service = ComputerService(computers)

    print(
        f"Загружено компьютеров из файла: "
        f"{len(computers)}"
    )

    choice = "-1"

    while choice != "0":
        print("\n===== КОМПЬЮТЕРНЫЙ МАГАЗИН =====")
        print("1. Добавить компьютер")
        print("2. Показать все компьютеры")
        print("3. Изменить компьютер")
        print("4. Найти компьютер")
        print("5. Фильтр по RAM")
        print("6. Сортировать по цене")
        print("7. Сохранить в JSON")
        print("8. Экспортировать в CSV")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            create_computer(service)

        elif choice == "2":
            service.show_computers()

        elif choice == "3":
            change_computer(service)

        elif choice == "4":
            find_computer(service)

        elif choice == "5":
            filter_computers(service)

        elif choice == "6":
            show_sorted_computers(service)

        elif choice == "7":
            save_json(service.computers)
            print("Данные сохранены в JSON.")

        elif choice == "8":
            export_csv(service.computers)
            print("Данные экспортированы в CSV.")

        elif choice == "0":
            save_json(service.computers)
            print("Данные сохранены.")
            print("Программа завершена.")

        else:
            print("Ошибка. Выберите пункт от 0 до 8.")


if __name__ == "__main__":
    main()