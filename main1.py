# Считает количество заказов выше средней стоимости
def above_average(orders, average):
    above_count = 0

    for price in orders:
        if price > average:
            above_count += 1

    return above_count


# Рассчитывает скидку и конечную стоимость заказа
def calculate_discount(price):
    discount = 0

    if price > 1500:
        discount = price * 0.1

    final_price = price - discount

    return discount, final_price


# Ввод одного набора заказов
def input_orders():
    orders = []

    count = int(input("Введите количество заказов: "))

    # Проверка количества заказов
    while count <= 0:
        print("Ошибка. Введите положительное число.")
        count = int(input("Введите количество заказов: "))

    # Ввод стоимости каждого заказа
    for i in range(count):
        price = float(input(f"Введите стоимость заказа {i + 1}: "))

        # Проверка стоимости заказа
        while price <= 0:
            print("Заказ не может быть отрицательным или равным 0.")
            price = float(input(f"Введите стоимость заказа {i + 1} повторно: "))

        orders.append(price)

    return orders


# Вывод основной статистики по одному набору
def show_statistics(orders, set_number):
    count = len(orders)

    total = sum(orders)
    average = total / count
    max_order = max(orders)
    min_order = min(orders)

    above_average_count = above_average(orders, average)

    print(f"\n===== Набор данных {set_number} =====")
    print(f"Количество заказов: {count}")
    print(f"Общая сумма: {total:.2f}")
    print(f"Средняя стоимость заказа: {average:.2f}")
    print(f"Максимальный заказ: {max_order:.2f}")
    print(f"Минимальный заказ: {min_order:.2f}")
    print(f"Заказов выше среднего: {above_average_count}")

    # Вывод скидки по каждому заказу
    for i in range(count):
        discount, final_price = calculate_discount(orders[i])

        print(
            f"Заказ {i + 1}. "
            f"Скидка: {discount:.2f}. "
            f"Конечная цена: {final_price:.2f}"
        )


# Дополнительный анализ всех наборов данных
def additional_analysis(data_sets):
    all_orders = []

    # Собираем все заказы из всех наборов
    for orders in data_sets:
        for price in orders:
            all_orders.append(price)

    total = sum(all_orders)
    average = total / len(all_orders)
    max_order = max(all_orders)
    min_order = min(all_orders)

    discounted_count = 0

    # Считаем количество заказов со скидкой
    for price in all_orders:
        if price > 1500:
            discounted_count += 1

    print("\n===== Дополнительный анализ =====")
    print(f"Количество наборов данных: {len(data_sets)}")
    print(f"Общее количество заказов: {len(all_orders)}")
    print(f"Общая сумма всех заказов: {total:.2f}")
    print(f"Средняя стоимость всех заказов: {average:.2f}")
    print(f"Максимальный заказ: {max_order:.2f}")
    print(f"Минимальный заказ: {min_order:.2f}")
    print(f"Количество заказов со скидкой: {discounted_count}")


# Основная функция программы
def main():
    # Список для хранения нескольких наборов заказов
    data_sets = []

    choice = "0"

    # Меню работает, пока пользователь не выберет 4
    while choice != "4":
        print("\n===== Анализ заказов интернет-магазина =====")
        print("1. Ввести новый набор данных")
        print("2. Показать статистику")
        print("3. Выполнить дополнительный анализ")
        print("4. Выход")

        choice = input("Выберите действие: ")

        # Ввод нового набора данных
        if choice == "1":
            orders = input_orders()
            data_sets.append(orders)

            print("Набор данных добавлен.")

        # Вывод статистики
        elif choice == "2":
            if len(data_sets) == 0:
                print("Сначала необходимо ввести данные.")
            else:
                for i in range(len(data_sets)):
                    show_statistics(data_sets[i], i + 1)

        # Дополнительный анализ
        elif choice == "3":
            if len(data_sets) == 0:
                print("Сначала необходимо ввести данные.")
            else:
                additional_analysis(data_sets)

        # Выход
        elif choice == "4":
            print("Программа завершена.")

        # Проверка неправильного пункта меню
        else:
            print("Ошибка. Выберите пункт от 1 до 4.")


# Запуск программы
if __name__ == "__main__":
    main()