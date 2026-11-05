# Лабораторная работа №16, вариант 15 - Медицинская клиника

Django, ORM, Admin, MTV, CRUD, шаблоны, ModelForm, CSRF, авторизация, статистика, история посещений, оптимизация запросов и 20 автоматических тестов.

## Быстрый запуск (Fish, Linux)

```fish
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -r requirements.txt
python manage.py makemigrations clinic
python manage.py migrate
python manage.py seed
python manage.py runserver
```

Откройте http://127.0.0.1:8000/ и http://127.0.0.1:8000/admin/.

Учебные аккаунты: `admin` / `Lab16Demo!2026` (администратор), `viewer` / `Lab16Demo!2026` (только просмотр). Пароли предназначены только для локальной учебной среды.

## Тесты

```fish
python manage.py test clinic -v 1
```

## PostgreSQL (дополнительно)

```fish
docker compose up -d
set -x POSTGRES_DB clinic16
set -x POSTGRES_USER clinic16
set -x POSTGRES_PASSWORD clinic16
set -x POSTGRES_HOST 127.0.0.1
set -x POSTGRES_PORT 5436
python manage.py migrate
python manage.py seed
```

## Архитектура

`config` - настройки и маршрутизация; `clinic/models.py` - пять моделей; `clinic/views.py` - представления; `clinic/forms.py` - формы; `clinic/admin.py` - административная панель; `templates` - HTML; `clinic/static` - CSS; `clinic/tests.py` - тесты; `clinic/management/commands/seed.py` - демонстрационные данные.

В `Appointment` связи `ForeignKey` с `Patient` и `Doctor`, `ManyToMany` с `Diagnosis`. Для устранения N+1 в списке применяются `select_related()` и `prefetch_related()`.

ORM: `all()`, `filter()`, `get()`, `order_by()`, `count()`, `exists()`, `aggregate()`, `annotate()`, `exclude()` доступны через Django QuerySet. Примеры в `orm_demo.py`.
