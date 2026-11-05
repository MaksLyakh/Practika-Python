from flask import Flask, send_from_directory
from pathlib import Path

app = Flask(__name__)


@app.get('/<path:name>')
def asset(name):
    response = send_from_directory(Path(__file__).parent / 'static', name)
    response.headers['Cache-Control'] = 'public, max-age=86400'
    response.headers['X-Content-Server'] = 'local-cdn-demo'
    return response


if __name__ == '__main__':
    app.run(port=5001)
