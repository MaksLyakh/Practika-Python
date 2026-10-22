import json
import socket

from exceptions import ProtocolError


MAX_MESSAGE_SIZE = 65536


def send_message(sock: socket.socket, data: dict) -> None:
    """Отправляет JSON-сообщение через TCP."""
    try:
        message = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8") + b"\n"

        if len(message) > MAX_MESSAGE_SIZE:
            raise ProtocolError("Сообщение слишком большое")

        sock.sendall(message)

    except (TypeError, ValueError) as error:
        raise ProtocolError(
            f"Ошибка сериализации JSON: {error}"
        ) from error


def receive_message(sock: socket.socket) -> dict:
    """Получает одно JSON-сообщение из TCP-потока."""
    buffer = bytearray()

    while True:
        chunk = sock.recv(1)

        if not chunk:
            raise ProtocolError("Соединение закрыто")

        if chunk == b"\n":
            break

        buffer.extend(chunk)

        if len(buffer) > MAX_MESSAGE_SIZE:
            raise ProtocolError("Сообщение слишком большое")

    try:
        data = json.loads(buffer.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ProtocolError(
            f"Некорректное JSON-сообщение: {error}"
        ) from error

    if not isinstance(data, dict):
        raise ProtocolError("JSON-сообщение должно быть объектом")

    return data
