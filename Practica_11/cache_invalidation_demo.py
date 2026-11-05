from app import create_app
from seed import seed


def main():
    seed()
    app = create_app()
    client = app.test_client()
    url = '/doctors/1/slots?date=2026-12-20'
    print('Первый запрос:', client.get(url).json)
    print('Повторный запрос:', client.get(url).json)
    response = client.post('/book', json={'patient_name': 'Демо', 'phone': '+79998887766',
        'doctor_id': 1, 'appointment_time': '2026-12-20 09:00', 'price': 1000})
    print('Новая запись:', response.status_code, response.json)
    print('После создания:', client.get(url).json)


if __name__ == '__main__':
    main()
