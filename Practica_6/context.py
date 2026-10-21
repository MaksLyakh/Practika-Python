from contextlib import contextmanager


@contextmanager
def operation(name: str):
    print(f"\n[CONTEXT] Начало операции: {name}")

    try:
        yield
    finally:
        print(f"[CONTEXT] Завершение операции: {name}")
