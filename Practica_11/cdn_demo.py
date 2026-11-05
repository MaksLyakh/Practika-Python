import requests


def inspect(url):
    try:
        response = requests.get(url, timeout=5)
        print('URL:', url)
        print('HTTP:', response.status_code, 'Байт:', len(response.content))
        for key in ('Cache-Control', 'Age', 'ETag', 'Last-Modified', 'Content-Type'):
            print(key + ':', response.headers.get(key, 'нет'))
    except requests.RequestException as error:
        print('Ошибка:', error)


if __name__ == '__main__':
    inspect('http://127.0.0.1:5000/static-files/doctor1.svg')
    inspect('http://127.0.0.1:5001/doctor1.svg')
