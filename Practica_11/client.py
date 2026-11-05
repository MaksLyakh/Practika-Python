import json
import requests

URL = 'http://127.0.0.1:5000'


def send(method, path, data=None):
    try:
        response = requests.request(method, URL + path, json=data, timeout=5)
        print('HTTP:', response.status_code)
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except requests.RequestException as error:
        print('Ошибка соединения:', error)


def main():
    while True:
        print('\n1 - Все записи | 2 - Запись по ID | 3 - Создать | 4 - Изменить статус')
        print('5 - Удалить | 6 - Врачи | 7 - Свободные часы | 8 - Записать нового пациента | 0 - Выход')
        choice = input('Выбор: ').strip()
        if choice == '0':
            break
        elif choice == '1':
            send('GET', '/appointments')
        elif choice == '2':
            send('GET', '/appointments/' + input('ID: '))
        elif choice == '3':
            data = {'doctor_id': int(input('ID врача: ')), 'patient_id': int(input('ID пациента: ')),
                    'appointment_time': input('Дата (2026-12-10 15:00): '), 'price': float(input('Цена: '))}
            send('POST', '/appointments', data)
        elif choice == '4':
            appointment_id = input('ID: ')
            send('PATCH', '/appointments/' + appointment_id, {'status': input('Статус (scheduled/completed/cancelled): ')})
        elif choice == '5':
            send('DELETE', '/appointments/' + input('ID: '))
        elif choice == '6':
            send('GET', '/doctors')
        elif choice == '7':
            doctor_id = input('ID врача: ')
            date = input('Дата (2026-12-10): ')
            send('GET', f'/doctors/{doctor_id}/slots?date={date}')
        elif choice == '8':
            data = {'patient_name': input('Имя: '), 'phone': input('Телефон: '),
                    'doctor_id': int(input('ID врача: ')), 'appointment_time': input('Дата и время: '),
                    'price': float(input('Цена: '))}
            send('POST', '/book', data)
        else:
            print('Нет такого пункта')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyboardInterrupt):
        print('Ввод прерван или неверное число')
