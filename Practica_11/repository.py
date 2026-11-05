from database import connect
from exceptions import NotFoundError, ValidationError
import sqlite3


class AppointmentRepository:
    def __init__(self, path=None):
        self.path = path

    def all(self, doctor_id=None, status=None):
        query = '''SELECT a.*, d.name AS doctor_name, p.name AS patient_name
                   FROM appointments a JOIN doctors d ON a.doctor_id=d.id
                   JOIN patients p ON a.patient_id=p.id WHERE 1=1'''
        params = []
        if doctor_id is not None:
            query += ' AND a.doctor_id=?'
            params.append(doctor_id)
        if status is not None:
            query += ' AND a.status=?'
            params.append(status)
        query += ' ORDER BY a.appointment_time, a.id'
        with connect(self.path) as db:
            return [dict(row) for row in db.execute(query, params)]

    def get(self, appointment_id):
        with connect(self.path) as db:
            row = db.execute('SELECT * FROM appointments WHERE id=?', (appointment_id,)).fetchone()
            if row is None:
                raise NotFoundError('Запись на приём не найдена')
            return dict(row)

    def create(self, data):
        try:
            with connect(self.path) as db:
                cursor = db.execute('''INSERT INTO appointments
                    (doctor_id, patient_id, appointment_time, status, price)
                    VALUES (?, ?, ?, ?, ?)''', (
                    data['doctor_id'], data['patient_id'], data['appointment_time'],
                    data.get('status', 'scheduled'), data['price']))
                appointment_id = cursor.lastrowid
            return self.get(appointment_id)
        except sqlite3.IntegrityError as error:
            raise ValidationError(f'Ошибка базы данных: {error}') from error

    def update(self, appointment_id, data, partial=False):
        old = self.get(appointment_id)
        fields = ('doctor_id', 'patient_id', 'appointment_time', 'status', 'price')
        required = ('doctor_id', 'patient_id', 'appointment_time', 'price')

        if not partial and any(field not in data for field in required):
            raise ValidationError('Для PUT нужно передать все обязательные поля записи')
 
        changes = {field: data[field] for field in fields if field in data}
        if not changes:
            raise ValidationError('Нет полей для изменения')
        try:
            with connect(self.path) as db:
                query = 'UPDATE appointments SET ' + ', '.join(f'{field}=?' for field in changes) + ' WHERE id=?'
                db.execute(query, [*changes.values(), appointment_id])
            return self.get(appointment_id)
        except sqlite3.IntegrityError as error:
            raise ValidationError(f'Ошибка базы данных: {error}') from error

    def delete(self, appointment_id):
        self.get(appointment_id)
        with connect(self.path) as db:
            db.execute('DELETE FROM appointments WHERE id=?', (appointment_id,))

    def doctors(self):
        with connect(self.path) as db:
            return [dict(row) for row in db.execute('SELECT * FROM doctors ORDER BY id')]

    def available_slots(self, doctor_id, date):
        with connect(self.path) as db:
            if db.execute('SELECT 1 FROM doctors WHERE id=?', (doctor_id,)).fetchone() is None:
                raise NotFoundError('Врач не найден')
            occupied = {row[0] for row in db.execute('''SELECT appointment_time FROM appointments
                WHERE doctor_id=? AND appointment_time LIKE ? AND status != 'cancelled' ''',
                (doctor_id, date + '%'))}
        return [f'{date} {hour:02d}:00' for hour in range(9, 18) if f'{date} {hour:02d}:00' not in occupied]

    def book_with_patient(self, patient_name, phone, doctor_id, appointment_time, price):
        # Оба INSERT выполняются в одной транзакции.
        try:
            with connect(self.path) as db:
                row = db.execute('SELECT id FROM patients WHERE phone=?', (phone,)).fetchone()
                if row:
                    patient_id = row['id']
                else:
                    patient_id = db.execute('INSERT INTO patients(name, phone) VALUES (?, ?)',
                                            (patient_name, phone)).lastrowid
                appointment_id = db.execute('''INSERT INTO appointments
                    (doctor_id, patient_id, appointment_time, price)
                    VALUES (?, ?, ?, ?)''', (doctor_id, patient_id, appointment_time, price)).lastrowid
            return self.get(appointment_id)
        except sqlite3.IntegrityError as error:
            raise ValidationError(f'Транзакция отменена: {error}') from error
