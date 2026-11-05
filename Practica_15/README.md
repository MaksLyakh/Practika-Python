# Лабораторная работа №15 - Flask, вариант 15 «Аптека»

Три связанные ORM-сущности: Medicine, Category, Purchase. HTML-интерфейс на Jinja2, REST API, CRUD, поиск, фильтрация по категории и диапазону цены, сортировка, покупки с уменьшением остатков, PostgreSQL, SQLAlchemy, Blueprint, Application Factory, обработка ошибок и логирование.

## Быстрый запуск (CachyOS / Fish)

```fish
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -r requirements.txt
cp .env.example .env
docker compose up -d
python seed.py
python run.py
```

Откройте http://127.0.0.1:5000

Если порт 5000 занят, измените port в run.py.

## Проверка

```fish
python -m pytest -q
curl http://127.0.0.1:5000/api/medicines
```

## API

- GET /api/medicines - список, параметры search, category, min_price, max_price, sort
- GET /api/medicines/1 - карточка
- POST /api/medicines - создание JSON {"name":"Препарат","price":120,"stock":10,"category_id":1}
- PUT /api/medicines/1 - полное обновление
- PATCH /api/medicines/1 - частичное обновление
- DELETE /api/medicines/1 - удаление
- GET /api/categories - категории
- GET /api/purchases - покупки
- POST /api/purchases - покупка JSON {"medicine_id":1,"quantity":2}

При покупке запас уменьшается, а запись появляется в истории. Удаление лекарства с покупками возвращает 409.

**Важно:** .env не добавлять в Git. Перед реальным развёртыванием заменить демонстрационные пароли и SECRET_KEY. Приложение учебное, не предназначено для промышленной эксплуатации.
