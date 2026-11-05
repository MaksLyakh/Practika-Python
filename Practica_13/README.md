# Лабораторная работа №13 - Вариант 15
## Медицинская клиника - приёмы. MongoDB + Redis

### Что реализовано
- MongoDB: база `clinic_lab13`, коллекция `appointment`, 24 тестовые записи.
- Документ: вложенные объекты `patient`, `doctor`, массив `prescriptions`, статус.
- CRUD, 10 видов запросов, 3 индекса (включая уникальный ID).
- Redis String (JSON), Hash (счётчик обращений), Sorted Set (ближайшие приёмы).
- Операции Redis: GET, SETEX, DELETE, TTL, HINCRBY, HGET, EXPIRE, ZADD, ZRANGE, SCAN.
- Cache-Aside с TTL 180 секунд и инвалидированием при изменении и удалении.
- Реальный бенчмарк MongoDB/Redis на 100, 1000, 10000 запросов.
- 23 изолированных теста с mongomock/fakeredis и отдельная проверка реальных баз.

### 1. Распаковка
Распакуйте ZIP в папку проекта, откройте эту папку в VS Code.

### 2. Python (Fish shell, CachyOS)
```fish
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -r requirements.txt
```
Если окружение уже создано в другой папке, лучше создать новое в этой папке.

### 3. Запуск баз данных
```fish
docker compose up -d
docker compose ps
```
MongoDB - `localhost:27017`, Redis - `localhost:6379`.
Существующий PostgreSQL из лабораторной №12 не затрагивается.
Данные MongoDB и Redis хранятся в Docker volumes.

### 4. Тесты без Docker (mock)
```fish
python -m pytest -v
```
Эти тесты используют mongomock/fakeredis, а не реальные серверы.

### 5. Проверка реальных серверов
```fish
python -m app.smoke
```
Ожидается строка `Проверка реальных баз: PASSED`.

### 6. Заполнение базы
```fish
python -m app.seed
```
Создаёт 24 записи. Повторный запуск не дублирует записи.

### 7. Меню приложения
```fish
python -m app.main
```
Пункт 12 демонстрирует Cache-Aside и инвалидирование.
Пример ID: `A001`, врач: `D01`, дата: `2026-12-10`.

### 8. Бенчмарк
```fish
python -m app.benchmark
```
Реальные измерения сохраняются в `benchmark_results.csv`.
Нельзя переносить в отчёт придуманные значения - используйте вывод своего ПК.

### 9. Дополнительные проверки через Docker
```fish
docker exec practica13-mongodb mongosh --quiet --eval 'db.adminCommand({ping:1})'
docker exec practica13-redis redis-cli ping
docker exec practica13-mongodb mongosh clinic_lab13 --quiet --eval 'db.appointment.countDocuments({})'
```

### 10. Индексы
- `unique_appointment_id` - уникальность ID записи.
- `doctor_schedule` - ускорение поиска расписания по врачу и дате.
- `status_date` - выборка ближайших запланированных приёмов.

### 11. Архитектура
CLI (`app/main.py`) -> Service (`app/service.py`) -> MongoRepository (`app/repository.py`) + RedisCache (`app/cache.py`).
Model и валидация - `app/models.py`.
Внешние подключения - `app/db.py`.

### 12. Остановка
```fish
docker compose down
```
Команда не удаляет данные. Не используйте `down -v`, если хотите сохранить записи.

### Замечание по безопасности
Базы опубликованы только на `127.0.0.1` и предназначены для локальной лабораторной работы без авторизации.
Для продакшена потребовались бы учётные записи, секреты и настройка сетевого доступа.
