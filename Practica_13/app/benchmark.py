import csv
from time import perf_counter
from app.db import connect

def measure(action, iterations):
    start = perf_counter()
    for _ in range(iterations):
        action()
    total_ms = (perf_counter() - start) * 1000
    return round(total_ms, 3), round(total_ms / iterations, 6)

def main():
    mongo, redis_client, service = connect()
    try:
        item = service.repo.collection.find_one({}, {"_id": 0})
        if item is None:
            print("Сначала выполните python -m app.seed")
            return
        aid = item["appointment_id"]
        key = service.cache.appointment_key(aid)
        service.cache.set_appointment(item)
        rows = []
        for n in (100, 1000, 10000):
            mongo_total, mongo_avg = measure(lambda: service.repo.get(aid), n)
            redis_total, redis_avg = measure(lambda: service.cache.get_appointment(aid), n)
            rows.extend([("MongoDB", n, mongo_total, mongo_avg), ("Redis", n, redis_total, redis_avg)])
        print(f"{'Источник':<12} {'Запросов':>8} {'Всего, мс':>14} {'Среднее, мс':>15}")
        for source, n, total, avg in rows:
            print(f"{source:<12} {n:>8} {total:>14.3f} {avg:>15.6f}")
        with open("benchmark_results.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["source", "requests", "total_ms", "average_ms"])
            writer.writerows(rows)
        print("Результаты сохранены в benchmark_results.csv")
    finally:
        mongo.close()
        redis_client.close()

if __name__ == "__main__":
    main()
