import logging
import os
import time

from flask import Flask, request, g, jsonify

from app.schemas import error_response


API_KEY = os.getenv("API_KEY", "secret-key")
CLIENT_VERSION = "1.0"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def register_middleware(app: Flask) -> None:
    """Регистрация обработчиков HTTP-запросов."""

    @app.before_request
    def before_request():
        g.start_time = time.perf_counter()

        logger.info(
            "Получен запрос: %s %s",
            request.method,
            request.path
        )

        # Документация и служебный маршрут доступны без ключа
        if request.path in ("/", "/openapi.yaml"):
            return None

        # Проверка версии клиента
        client_version = request.headers.get("X-Client-Version")

        if client_version != CLIENT_VERSION:
            return jsonify(error_response(
                "Отсутствует или неверен заголовок X-Client-Version",
                400
            )), 400

        # Проверка API-ключа
        api_key = request.headers.get("X-API-Key")

        if api_key != API_KEY:
            return jsonify(error_response(
                "Неверный или отсутствующий API-ключ",
                401
            )), 401

        return None

    @app.after_request
    def after_request(response):
        start_time = getattr(
            g,
            "start_time",
            time.perf_counter()
        )

        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            "%s %s -> %s -> %.2f ms",
            request.method,
            request.path,
            response.status_code,
            duration_ms
        )

        response.headers["X-Response-Time"] = (
            f"{duration_ms:.2f} ms"
        )

        response.headers["X-Server-Version"] = "1.0"

        return response
