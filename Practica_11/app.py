import os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from database import init_database
from repository import AppointmentRepository
from service import ClinicService
from cache import ScheduleCache
from exceptions import ValidationError, NotFoundError


def create_app(db_path=None):
    app = Flask(__name__)
    app.json.ensure_ascii = False
    init_database(db_path)
    repo = AppointmentRepository(db_path)
    service = ClinicService(repo)
    cache = ScheduleCache()

    @app.errorhandler(ValidationError)
    def invalid(error):
        return jsonify(error=str(error)), 400

    @app.errorhandler(NotFoundError)
    def missing(error):
        return jsonify(error=str(error)), 404

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(error='Маршрут не найден'), 404

    @app.get('/')
    def home():
        return jsonify(message='Клиника - лабораторная 11, вариант 15', endpoints='/appointments, /doctors, /doctors/1/slots?date=2026-12-10')

    @app.get('/appointments')
    def all_appointments():
        doctor_id = request.args.get('doctor_id', type=int)
        status = request.args.get('status')
        result = repo.all(doctor_id, status)
        sort = request.args.get('sort')
        if sort == 'price':
            result.sort(key=lambda row: row['price'])
        if sort == '-price':
            result.sort(key=lambda row: row['price'], reverse=True)
        return jsonify(result)

    @app.get('/appointments/<int:appointment_id>')
    def get_appointment(appointment_id):
        return jsonify(repo.get(appointment_id))

    @app.post('/appointments')
    def create_appointment():
        result = service.create(request.get_json(silent=True))
        cache.invalidate(result['doctor_id'])
        return jsonify(result), 201

    @app.put('/appointments/<int:appointment_id>')
    def replace_appointment(appointment_id):
        old = repo.get(appointment_id)
        result = service.update(appointment_id, request.get_json(silent=True))
        cache.invalidate(old['doctor_id'])
        cache.invalidate(result['doctor_id'])
        return jsonify(result)

    @app.patch('/appointments/<int:appointment_id>')
    def edit_appointment(appointment_id):
        old = repo.get(appointment_id)
        result = service.update(appointment_id, request.get_json(silent=True), partial=True)
        cache.invalidate(old['doctor_id'])
        cache.invalidate(result['doctor_id'])
        return jsonify(result)

    @app.delete('/appointments/<int:appointment_id>')
    def delete_appointment(appointment_id):
        old = repo.get(appointment_id)
        repo.delete(appointment_id)
        cache.invalidate(old['doctor_id'])
        return jsonify(message='Запись удалена')

    @app.get('/doctors')
    def doctors():
        return jsonify(repo.doctors())

    @app.get('/doctors/<int:doctor_id>/slots')
    def slots(doctor_id):
        date = request.args.get('date', '')
        try:
            from datetime import datetime
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Укажите date в формате ГГГГ-ММ-ДД')
        key = f'slots:{doctor_id}:{date}'
        result = cache.get(key)
        source = 'redis' if result is not None else 'sqlite'
        if result is None:
            result = repo.available_slots(doctor_id, date)
            cache.set(key, result)
        return jsonify(doctor_id=doctor_id, date=date, slots=result, source=source)

    @app.post('/book')
    def book():
        result = service.book(request.get_json(silent=True))
        cache.invalidate(result['doctor_id'])
        return jsonify(result), 201

    @app.get('/static-files/<path:name>')
    def static_files(name):
        response = send_from_directory(Path(__file__).parent / 'static', name)
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response

    return app


if __name__ == '__main__':
    create_app().run(port=int(os.getenv('PORT', '5000')), debug=False)
