# Лабораторная работа №14 - Вариант 15
## Медицинская клиника - REST API на FastAPI

### Реализовано
- `GET /appointments`, `GET /appointments/{id}`, `POST /appointments`, `PUT /appointments/{id}`, `PATCH /appointments/{id}`, `DELETE /appointments/{id}`
- `GET /appointments/search`, `GET /appointments/statistics`
- Фильтрация, сортировка asc/desc, поиск и пагинация
- PostgreSQL 16, SQLAlchemy 2, Pydantic 2, Dependency Injection
- Redis Cache-Aside, TTL 180 секунд, инвалидирование, Pub/Sub событий
- JWT-регистрация, вход, профиль, роли USER (чтение) и ADMIN (CRUD)
- BackgroundTasks для логирования создания
- Загрузка и скачивание вложений до 2 МБ (pdf, txt, png, jpg, jpeg)
- Асинхронный SQLAlchemy с asyncpg: `GET /async/statistics`
- Внешний API: `GET /external-data` (нужен интернет)
- Swagger `/docs`, ReDoc `/redoc`, OpenAPI `/openapi.json`
- 33 автоматических теста (SQLite в памяти, поддельный кэш)

### 1. Распаковка и установка (CachyOS, Fish)

Откройте распакованную папку `Practica_14_Variant_15` в VS Code.
В терминале из этой папки:

```fish
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -r requirements.txt
```

### 2. Запуск PostgreSQL и Redis

```fish
docker compose up -d
docker compose ps
```

**Важно:** используются порты `5434` (PostgreSQL) и `6380` (Redis), чтобы не конфликтовать с лабораторными №12 и №13. Никакие старые контейнеры не удаляются.

### 3. Настройки

```fish
cp .env.example .env
```

В `.env` **обязательно поменяйте** `JWT_SECRET` на длинную случайную строку и `ADMIN_PASSWORD` на свой пароль **до** запуска `app.seed`.
Для локальной учебной работы значения в `.env.example` подходят только как демонстрация.

### 4. Создание таблиц и 24 записей

```fish
python -m app.seed
```

При первом запуске создаются ADMIN и 24 приёма. Повторное заполнение не создаёт дубликатов.
Логин администратора по умолчанию: `admin`, пароль берётся из `.env`.

### 5. Автоматические тесты

```fish
python -m pytest -v
```

Тесты изолированы: SQLite в памяти и тестовый кэш, не реальный PostgreSQL и Redis. Ожидается `33 passed`, если окружение совместимо.

### 6. Запуск API

```fish
python -m uvicorn app.main:app --reload
```

Откройте:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Проверка: http://127.0.0.1:8000/health

### 7. Авторизация в Swagger

1. `POST /auth/login` -> Try it out -> тело JSON:
   `{"username":"admin","password":"<ваш ADMIN_PASSWORD>"}`
2. Скопируйте `access_token` из ответа.
3. Нажмите `Authorize` в верхней части Swagger и вставьте токен.
4. После этого доступны все операции CRUD.

`POST /auth/register` создаёт пользователя с ролью USER: он может читать, но не изменять приёмы.

### 8. Пример JSON для POST /appointments

```json
{
  "patient": "Алексей Иванов",
  "doctor": "Иван Иванов",
  "specialty": "Терапевт",
  "date": "2026-12-20",
  "time": "10:30:00",
  "room": 101,
  "status": "scheduled"
}
```

Ожидаемый код: `201 Created`. Полученный `id` используйте для GET, PUT, PATCH и DELETE.
Пример PATCH: `{"status":"completed"}`.

### 9. Проверка Cache-Aside

После создания приёма выполните `GET /appointments/{id}` дважды.
Первый GET заполняет Redis, второй читает из кэша.
Измените запись через PATCH: Redis-ключ удалится.
Следующий GET получит новые данные из PostgreSQL и снова сохранит в Redis.

Можно проверить ключ:
```fish
docker exec practica14-redis redis-cli KEYS 'lab14:appointment:*'
```

### 10. Проверка асинхронного доступа

В Swagger откройте `GET /async/statistics`. Он использует асинхронный движок SQLAlchemy с драйвером asyncpg.
`GET /external-data` обращается к публичному API GitHub и требует подключения к интернету.

### 11. Проверка реального API

Когда Uvicorn запущен, в **другом** терминале:
```fish
source .venv/bin/activate.fish
python -m app.smoke
```

Скрипт проверяет реальный API с PostgreSQL и Redis, создаёт временную запись и удаляет её.

### 12. Завершение

Остановить Uvicorn: `Ctrl+C`.
Остановить контейнеры, сохранив данные:
```fish
docker compose down
```

### Архитектура
`Router -> Service -> Repository -> SQLAlchemy -> PostgreSQL`.
Redis доступен через `Cache`, Pydantic проверяет запросы, `security.py` проверяет JWT и роли.

### Замечания
- Приложение учебное: контейнеры доступны только с localhost, стандартные учётные данные необходимо заменить.
- Файлы хранятся на локальном диске, в PostgreSQL хранится их метаинформация.
- Внешний API может быть недоступен без интернета; это не мешает основным функциям.
- Реальный запуск на компьютере пользователя необходимо подтвердить отдельно; прохождение 33 тестов проверяет изолированную логику API.
