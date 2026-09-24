from models import Computer, GamingComputer, OfficeComputer

from operations import (
    filter_by_ram,
    get_names,
    sort_by_price,
    most_expensive,
    has_ram,
    get_processors,
    total_price,
    process
)

from generators import computers_by_type, ComputerIterator


def show_computers(computers):
    if len(computers) == 0:
        print("Список компьютеров пуст.")
        return

    for i, computer in enumerate(computers, 1):
        print(f"{i}. {computer}")


def input_number(message, number_type=int):
    while True:
        try:
            number = number_type(input(message))

            if number <= 0:
                print("Число должно быть больше 0.")
                continue

            return number

        except ValueError:
            print("Ошибка. Введите корректное число.")


def add_computer(computers):
    print("\nТип компьютера:")
    print("1. Обычный")
    print("2. Игровой")
    print("3. Офисный")

    computer_type = input("Выберите тип: ")

    if computer_type not in ("1", "2", "3"):
        print("Неверный тип компьютера.")
        return

    name = input("Название: ")
    processor = input("Процессор: ")

    ram = input_number("RAM (ГБ): ")
    storage = input_number("Накопитель (ГБ): ")
    price = input_number("Цена: ", float)

    if computer_type == "1":
        computer = Computer(
            name, processor, ram, storage, price
        )

    elif computer_type == "2":
        computer = GamingComputer(
            name, processor, ram, storage, price
        )

    else:
        computer = OfficeComputer(
            name, processor, ram, storage, price
        )

    computers.append(computer)

    print("Компьютер добавлен.")


def show_generator(computers):
    print("\nДоступные типы:")
    print("Обычный")
    print("Игровой")
    print("Офисный")

    computer_type = input("Введите тип компьютера: ")

    found = False

    for computer in computers_by_type(
        computers,
        computer_type
    ):
        print(computer)
        found = True

    if not found:
        print("Компьютеры такого типа не найдены.")


def show_iterator(computers):
    iterator = iter(
        ComputerIterator(computers)
    )

    print("\nПоследовательный вывод компьютеров:")

    while True:
        try:
            computer = next(iterator)
            print(computer)

        except StopIteration:
            print("Итерация завершена.")
            break


def show_pipeline(computers):
    if len(computers) == 0:
        print("Список компьютеров пуст.")
        return

    print("\nПервый конвейер:")
    print("Компьютеры с RAM от 16 ГБ, сортировка по цене")

    result = process(
        computers,
        lambda computer: computer.ram >= 16,
        lambda computer: (
            computer.price,
            computer.name
        ),
        lambda item: item[0]
    )

    for price, name in result:
        print(f"{name}: {price:.2f} руб.")

    print("\nВторой конвейер:")
    print("Игровые компьютеры, сортировка названий")

    result = process(
        computers,
        lambda computer: computer.get_type() == "Игровой",
        lambda computer: computer.name,
        lambda name: name
    )

    for name in result:
        print(name)


def main():
    computers = [
        GamingComputer(
            "Gaming Pro",
            "Intel Core i7",
            32,
            1000,
            125000
        ),

        GamingComputer(
            "Gaming Lite",
            "AMD Ryzen 5",
            16,
            512,
            78000
        ),

        OfficeComputer(
            "Office Mini",
            "Intel Core i3",
            8,
            256,
            35000
        ),

        OfficeComputer(
            "Office Plus",
            "Intel Core i5",
            16,
            512,
            57000
        ),

        Computer(
            "Home PC",
            "AMD Ryzen 5",
            16,
            512,
            49000
        )
    ]

    choice = "-1"

    while choice != "0":

        print("\n===== КАТАЛОГ КОМПЬЮТЕРОВ =====")
        print("1. Показать все компьютеры")
        print("2. Добавить компьютер")
        print("3. Фильтрация по RAM")
        print("4. Получить названия компьютеров")
        print("5. Сортировка по цене")
        print("6. Самый дорогой компьютер")
        print("7. Проверка наличия заданной RAM")
        print("8. Показать уникальные процессоры")
        print("9. Общая стоимость компьютеров")
        print("10. Генератор по типу компьютера")
        print("11. Собственный итератор")
        print("12. Конвейер обработки данных")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_computers(computers)

        elif choice == "2":
            add_computer(computers)

        elif choice == "3":
            ram = input_number(
                "Минимальный объём RAM (ГБ): "
            )

            result = filter_by_ram(
                computers,
                ram
            )

            show_computers(result)

        elif choice == "4":
            names = get_names(computers)

            for name in names:
                print(name)

        elif choice == "5":
            result = sort_by_price(computers)
            show_computers(result)

        elif choice == "6":
            computer = most_expensive(computers)

            if computer is None:
                print("Список компьютеров пуст.")
            else:
                print(computer)

        elif choice == "7":
            ram = input_number(
                "Введите объём RAM (ГБ): "
            )

            if has_ram(computers, ram):
                print("Компьютер с такой RAM найден.")
            else:
                print("Компьютер с такой RAM не найден.")

        elif choice == "8":
            processors = get_processors(computers)

            for processor in sorted(processors):
                print(processor)

        elif choice == "9":
            print(
                f"Общая стоимость: "
                f"{total_price(computers):.2f} руб."
            )

        elif choice == "10":
            show_generator(computers)

        elif choice == "11":
            show_iterator(computers)

        elif choice == "12":
            show_pipeline(computers)

        elif choice == "0":
            print("Программа завершена.")

        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()