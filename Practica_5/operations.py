from functools import reduce


# Универсальная фильтрация
def filter_objects(objects, predicate):
    return filter(predicate, objects)


# Универсальное преобразование
def transform_objects(objects, operation):
    return map(operation, objects)


# Универсальная сортировка
def sort_objects(objects, key_function, reverse=False):
    return sorted(
        objects,
        key=key_function,
        reverse=reverse
    )


# Фильтрация компьютеров по RAM
def filter_by_ram(computers, min_ram):
    return list(
        filter_objects(
            computers,
            lambda computer: computer.ram >= min_ram
        )
    )


# Получение названий компьютеров
def get_names(computers):
    return list(
        transform_objects(
            computers,
            lambda computer: computer.name
        )
    )


# Сортировка компьютеров по цене
def sort_by_price(computers):
    return sort_objects(
        computers,
        lambda computer: computer.price
    )


# Поиск самого дорогого компьютера
def most_expensive(computers):
    if len(computers) == 0:
        return None

    return max(
        computers,
        key=lambda computer: computer.price
    )


# Проверка наличия компьютера с заданной RAM
def has_ram(computers, ram):
    return any(
        computer.ram == ram
        for computer in computers
    )


# Получение списка уникальных процессоров
def get_processors(computers):
    return {
        computer.processor
        for computer in computers
    }


# Расчёт общей стоимости компьютеров
def total_price(computers):
    return reduce(
        lambda total, computer: total + computer.price,
        computers,
        0
    )


# Универсальный конвейер обработки данных
def process(computers, predicate, transform, key_function):
    filtered = filter_objects(
        computers,
        predicate
    )

    transformed = transform_objects(
        filtered,
        transform
    )

    sorted_objects = sort_objects(
        transformed,
        key_function
    )

    for obj in sorted_objects:
        yield obj