from datetime import datetime
from exceptions import ValidationError


class ClinicService:
    def __init__(self, repository):
        self.repository = repository

    def validate(self, data, partial=False):
        if not isinstance(data, dict):
            raise ValidationError('Ожидается JSON-объект')
        fields = ('doctor_id', 'patient_id', 'appointment_time', 'price')
        if not partial and any(field not in data for field in fields):
            raise ValidationError('Не все обязательные поля заполнены')
        for field in ('doctor_id', 'patient_id'):
            if field in data and (type(data[field]) is not int or data[field] <= 0):
                raise ValidationError(f'{field} должен быть положительным целым числом')
        if 'price' in data and (type(data['price']) not in (int, float) or not 0 <= data['price'] < float('inf')):
            raise ValidationError('Цена должна быть неотрицательным числом')
        if 'appointment_time' in data:
            try:
                datetime.strptime(data['appointment_time'], '%Y-%m-%d %H:%M')
            except (ValueError, TypeError):
                raise ValidationError('Дата должна быть в формате ГГГГ-ММ-ДД ЧЧ:ММ')
        if 'status' in data and data['status'] not in ('scheduled', 'completed', 'cancelled'):
            raise ValidationError('Неизвестный статус')
        if any(key not in (*fields, 'status') for key in data):
            raise ValidationError('Переданы неизвестные поля')

    def create(self, data):
        self.validate(data)
        return self.repository.create(data)

    def update(self, appointment_id, data, partial=False):
        self.validate(data, partial=partial)
        return self.repository.update(appointment_id, data, partial)

    def book(self, data):
        if not isinstance(data, dict):
            raise ValidationError('Неверный формат запроса')
        if not isinstance(data.get('patient_name'), str) or not data['patient_name'].strip():
            raise ValidationError('Укажите имя пациента')
        if not isinstance(data.get('phone'), str) or not data['phone'].strip():
            raise ValidationError('Укажите телефон')
        details = {k: data.get(k) for k in ('doctor_id', 'appointment_time', 'price')}
        self.validate({**details, 'patient_id': 1})
        return self.repository.book_with_patient(data['patient_name'].strip(), data['phone'].strip(),
                                                 details['doctor_id'], details['appointment_time'], details['price'])
