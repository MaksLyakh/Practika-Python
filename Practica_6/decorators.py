import time
from functools import wraps


# Декоратор для журналирования вызовов
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Вызвана функция {func.__name__}")
        result = func(*args, **kwargs)
        return result

    return wrapper


# Декоратор для измерения времени выполнения
def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()
        print(f"[TIME] {func.__name__}: {end - start:.6f} сек.")

        return result

    return wrapper


# Декоратор с параметром
def repeat(count: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None

            for _ in range(count):
                result = func(*args, **kwargs)

            return result

        return wrapper

    return decorator
