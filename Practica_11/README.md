# Лабораторная работа №11, вариант 15 - Медицинская клиника

Тема: реляционные и нереляционные базы данных, SQL, Redis, MongoDB и CDN.

## Подготовка (Linux / Windows)

Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py
python app.py
```

На Windows активация: `.venv\Scripts\activate`.

В **другом терминале**:

```bash
python client.py
```

Сервер: http://127.0.0.1:5000

## Проверка REST API

Открой в браузере:

- http://127.0.0.1:5000/appointments
- http://127.0.0.1:5000/doctors
- http://127.0.0.1:5000/appointments/1
- http://127.0.0.1:5000/doctors/1/slots?date=2026-12-10
- http://127.0.0.1:5000/static-files/doctor1.svg

В клиенте проверь пункты 1-8. Создай запись на свободное время, измени статус, удали. Запрос `/appointments/99999` покажет ошибку 404.

## SQL

`sql/schema.sql` - 5 таблиц, первичные и внешние ключи, связи 1:N и N:M, ограничения и 3 индекса.

`sql/queries.sql` - 16 SQL-запросов. **Внимание:** запросы INSERT, UPDATE, DELETE меняют данные; запускай их на копии БД.

Для выполнения запросов открой `clinic.db` в DB Browser for SQLite или SQLite CLI:

```bash
sqlite3 clinic.db
```

Можно вставлять запросы из `sql/queries.sql` по одному. Для демонстрации плана выполнения:

```sql
EXPLAIN QUERY PLAN SELECT * FROM appointments WHERE doctor_id=1 ORDER BY appointment_time;
```

## Тесты

```bash
python -m pytest tests -v
```

## Redis и MongoDB

Для дополнительных частей требуется Docker и Docker Compose:

```bash
docker compose up -d
python nosql_demo.py
python benchmark.py
python cache_invalidation_demo.py
```

Redis хранит расписание свободных часов с TTL 60 секунд, ключ `slots:<doctor_id>:<date>`. Второй запрос возвращает `source: redis`, если Redis работает. После создания/изменения/удаления записи кэш врача сбрасывается.

MongoDB хранит отдельную демонстрационную коллекцию расписаний; выполняются insert/find/update/count/delete.

Для эксперимента с распределённым кэшем запусти два API с разными портами:

```bash
PORT=5000 python app.py
PORT=5002 python app.py
```

Оба используют один Redis, ключи общие. Для корректной общей SQL-БД при нескольких процессах используется один и тот же файл `clinic.db`.

## Локальная имитация CDN

В отдельном терминале:

```bash
python cdn_server.py
python cdn_demo.py
```

Адреса:

- origin: http://127.0.0.1:5000/static-files/doctor1.svg
- локальный CDN: http://127.0.0.1:5001/doctor1.svg
- ещё ресурсы: `/doctor2.svg`, `/doctor3.svg`, `/therapy.svg`

Сравни HTTP-заголовки `Cache-Control` и `Content-Type`. Это **локальная имитация**, не настоящий геораспределённый CDN.

Версионирование: создай копию `doctor1.svg` под именем `doctor1.v2.svg`, измени содержимое и сравни URL. Версия в имени предотвращает использование старого закэшированного ресурса.

## Дополнительные задания

1. MongoDB - `nosql_demo.py`.
2. Распределённый Redis - два экземпляра API, общий Redis.
3. Сброс кэша - `cache_invalidation_demo.py`.
4. Версии CDN-файлов - `static/doctor1.v1.svg` и `static/doctor1.v2.svg`.
5. Benchmark - `benchmark.py`.
6. EXPLAIN - `benchmark.py` и SQL-запрос выше.
7. Docker Compose - `docker-compose.yml` для Redis/MongoDB.
8. Репликация - теоретическая схема в `EXTRAS.md` (настоящая репликация не требуется по методичке).

## Скриншоты для отчёта

1. Структура проекта в VS Code.
2. `python seed.py` и `python app.py`.
3. GET списка записей и врачей.
4. Клиент: создание записи.
5. Клиент: PATCH статуса.
6. Клиент: удаление и 404 для удалённого ID.
7. Свободные слоты до/после записи.
8. SQLite: таблицы, связи и SQL JOIN / GROUP BY / EXPLAIN.
9. `python -m pytest tests -v`.
10. `docker compose up -d` и `python nosql_demo.py`.
11. Redis: два запроса к слоту, источники `sqlite` и `redis`.
12. CDN: оба сервера и `python cdn_demo.py`.
13. `python benchmark.py`.

Не делай скриншоты с ошибками подключения, пока не запущены нужные сервисы.
