# Лабораторная работа №10

## REST API медицинской клиники

**Вариант:** 15  
**Язык программирования:** Python  
**Фреймворк:** Flask

## Цель работы

Изучить разработку REST API на Python с использованием
Flask, реализовать обработку HTTP-запросов и работу
с данными в оперативной памяти.

## Описание проекта

Приложение предназначено для управления записями
пациентов на приём к врачу.

Каждая запись содержит следующие данные:

- ID записи;
- пациент;
- врач;
- специальность;
- дата;
- время;
- кабинет;
- статус записи.

Данные хранятся в оперативной памяти без использования
базы данных.

## Возможности приложения

- Создание записей на приём.
- Получение всех записей и поиск по ID.
- Полное и частичное обновление записей.
- Удаление записей.
- Фильтрация и сортировка.
- Поиск записей по пациенту.
- Просмотр записей конкретного врача.
- Получение статистики.
- Пагинация результатов.
- Проверка API-ключа.
- Проверка версии клиента.
- Логирование HTTP-запросов.
- Поддержка ETag.
- Документация OpenAPI.
- Запуск приложения в Docker.
- Автоматическое тестирование с pytest.

## Структура проекта

```text
lab10/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── repository.py
│   ├── service.py
│   ├── routes.py
│   ├── schemas.py
│   ├── exceptions.py
│   ├── middleware.py
│   └── openapi.yaml
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_service.py
│   └── test_repository.py
├── app.py
├── client.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Установка

Создать виртуальное окружение:

```bash
python -m venv .venv
```

Активировать окружение в Fish:

```bash
source .venv/bin/activate.fish
```

Установить зависимости:

```bash
python -m pip install -r requirements.txt
```

## Запуск сервера

```bash
python app.py
```

Сервер будет доступен по адресу:

http://127.0.0.1:5000

## Запуск клиента

В отдельном терминале выполнить:

```bash
python client.py
```

Клиент предоставляет консольное меню для выполнения
операций с записями пациентов.

## HTTP-заголовки

Для обращения к защищённым маршрутам API необходимо
передавать заголовки:

```text
X-API-Key: secret-key
X-Client-Version: 1.0
```

## Основные маршруты

| Метод | Маршрут | Назначение |
|---|---|---|
| GET | /appointments | Получение списка |
| GET | /appointments/{id} | Получение по ID |
| POST | /appointments | Создание |
| PUT | /appointments/{id} | Полное обновление |
| PATCH | /appointments/{id} | Частичное обновление |
| DELETE | /appointments/{id} | Удаление |
| GET | /appointments/search | Поиск пациента |
| GET | /appointments/available | Запланированные приёмы |
| GET | /appointments/stats | Статистика |
| GET | /appointments/doctor/{doctor} | Записи врача |

## Документация API

Спецификация OpenAPI доступна по адресу:

http://127.0.0.1:5000/openapi.yaml

## Тестирование

Для запуска автоматических тестов:

```bash
python -m pytest -v
```

## Docker

Сборка образа:

```bash
sudo docker build -t clinic-api .
```

Запуск контейнера:

```bash
sudo docker run --rm \
  -p 127.0.0.1:5000:5000 \
  -e HOST=0.0.0.0 \
  clinic-api
```

## Используемые технологии

- Python
- Flask
- requests
- pytest
- OpenAPI 3.0
- Docker
