from pathlib import Path

from flask import Flask, jsonify, send_file

from app.routes import appointments_bp
from app.middleware import register_middleware
from app.schemas import error_response


def create_app() -> Flask:
    app = Flask(__name__)

    # Подключаем маршруты API
    app.register_blueprint(appointments_bp)

    # Подключаем Middleware
    register_middleware(app)

    @app.route("/")
    def index():
        return jsonify({
            "message": "REST API медицинской клиники",
            "version": "1.0",
            "resource": "/appointments",
            "documentation": "/openapi.yaml"
        }), 200

    @app.route("/openapi.yaml")
    def openapi():
        file_path = Path(__file__).parent / "openapi.yaml"

        return send_file(
            file_path,
            mimetype="application/yaml"
        )

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(error_response(
            "Запрашиваемый ресурс не найден",
            404
        )), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(error_response(
            "HTTP-метод не поддерживается",
            405
        )), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify(error_response(
            "Внутренняя ошибка сервера",
            500
        )), 500

    return app
