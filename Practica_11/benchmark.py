import time
from database import connect
from cache import ScheduleCache


def benchmark():
    cache = ScheduleCache()
    key = 'benchmark:doctors'
    with connect() as db:
        start = time.perf_counter()
        for _ in range(100):
            db.execute('SELECT * FROM doctors').fetchall()
        sql_time = time.perf_counter() - start
    print(f'SQLite 100 запросов: {sql_time:.5f} с')
    if cache.redis is not None:
        cache.set(key, ['doctor1', 'doctor2'])
        start = time.perf_counter()
        for _ in range(100):
            cache.get(key)
        print(f'Redis 100 запросов: {time.perf_counter()-start:.5f} с')
        cache.redis.delete(key)
    else:
        print('Redis недоступен, сравнение пропущено')
    with connect() as db:
        for row in db.execute('EXPLAIN QUERY PLAN SELECT * FROM appointments WHERE doctor_id=1 ORDER BY appointment_time'):
            print('EXPLAIN:', tuple(row))


if __name__ == '__main__':
    benchmark()
