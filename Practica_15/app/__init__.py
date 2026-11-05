import logging
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from .database import engine, Base, SessionLocal
from . import models
from .routes.web import web
from .routes.api import api

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-only')
    if test_config:
        app.config.update(test_config)
    logging.basicConfig(filename='lab15.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix='/api')
    @app.before_request
    def log_request():
        app.logger.info('%s %s', request.method, request.path)
    @app.errorhandler(404)
    def missing(err):
        if request.path.startswith('/api/'):
            return jsonify(error='Не найдено'), 404
        return render_template('404.html'), 404
    @app.errorhandler(400)
    def bad(err):
        if request.path.startswith('/api/'):
            return jsonify(error='Некорректные данные'), 400
        return render_template('error.html', message='Некорректные данные'), 400
    @app.errorhandler(409)
    def conflict(err):
        if request.path.startswith('/api/'):
            return jsonify(error='Конфликт данных'), 409
        return render_template('error.html', message='Конфликт данных'), 409
    @app.errorhandler(500)
    def server_error(err):
        app.logger.exception('Внутренняя ошибка')
        if request.path.startswith('/api/'):
            return jsonify(error='Внутренняя ошибка'), 500
        return render_template('error.html', message='Внутренняя ошибка сервера'), 500
    with app.app_context():
        Base.metadata.create_all(bind=engine)
    app.logger.info('Flask запущен')
    return app
