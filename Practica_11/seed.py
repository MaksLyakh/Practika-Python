from database import connect, init_database


def seed(path=None):
    init_database(path)
    with connect(path) as db:
        db.executemany('INSERT OR IGNORE INTO departments VALUES (?, ?, ?)', [
            (1, 'Терапия', 'therapy.svg'), (2, 'Диагностика', 'diagnostics.svg'),
            (3, 'Хирургия', 'surgery.svg'), (4, 'Педиатрия', 'pediatrics.svg'),
            (5, 'Кардиология', 'cardiology.svg')])
        db.executemany('INSERT OR IGNORE INTO doctors VALUES (?, ?, ?, ?)', [
            (1, 'Иванов Иван', 'Терапевт', 'doctor1.svg'),
            (2, 'Петрова Анна', 'Кардиолог', 'doctor2.svg'),
            (3, 'Сидоров Павел', 'Хирург', 'doctor3.svg'),
            (4, 'Кузнецова Мария', 'Педиатр', 'doctor1.svg'),
            (5, 'Орлов Дмитрий', 'Терапевт', 'doctor2.svg')])
        db.executemany('INSERT OR IGNORE INTO patients VALUES (?, ?, ?)', [
            (1, 'Алексей Смирнов', '+79000000001'),
            (2, 'Елена Иванова', '+79000000002'),
            (3, 'Максим Петров', '+79000000003'),
            (4, 'Ольга Соколова', '+79000000004'),
            (5, 'Андрей Морозов', '+79000000005')])
        db.executemany('INSERT OR IGNORE INTO doctor_departments VALUES (?, ?)', [
            (1, 1), (1, 2), (2, 5), (2, 2), (3, 3), (4, 4), (5, 1), (5, 2)])
        db.executemany('INSERT OR IGNORE INTO appointments VALUES (?, ?, ?, ?, ?, ?)', [
            (i, (i-1)%5+1, (i+1)%5+1, f'2026-12-{(i-1)//5+10:02d} {9+(i-1)%5:02d}:00',
             'scheduled', 1000 + i*150) for i in range(1, 11)])
    print('Тестовые данные добавлены: 5 врачей, 5 пациентов, 10 записей')


if __name__ == '__main__':
    seed()
