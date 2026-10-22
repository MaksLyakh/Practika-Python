import logging
import socket
import threading

from exceptions import InsuranceError, ProtocolError
from protocol import receive_message, send_message
from repository import PolicyRepository
from service import InsuranceService


HOST = "127.0.0.1"
PORT = 5000
CLIENT_TIMEOUT = 60

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger(__name__)

repository = PolicyRepository()
service = InsuranceService(repository)

repository_lock = threading.RLock()


def process_request(request: dict) -> dict:
    """Обрабатывает JSON-запрос клиента."""
    try:
        command = request.get("command")
        data = request.get("data", {})

        if not isinstance(data, dict):
            raise ProtocolError("Поле data должно быть объектом")

        with repository_lock:
            if command == "create_policy":
                result = service.create_policy(
                    policy_id=data["policy_id"],
                    client_name=data["client_name"],
                    insurance_type=data["insurance_type"],
                    amount=data["amount"],
                    duration_months=data["duration_months"]
                )

            elif command == "get_policy":
                result = service.get_policy(
                    data["policy_id"]
                )

            elif command == "get_all_policies":
                result = service.get_all_policies()

            elif command == "update_status":
                result = service.update_status(
                    data["policy_id"],
                    data["status"]
                )

            elif command == "delete_policy":
                result = service.delete_policy(
                    data["policy_id"]
                )

            elif command == "find_by_client":
                result = service.find_by_client(
                    data["client_name"]
                )

            elif command == "calculate_cost":
                result = service.calculate_cost(
                    data["policy_id"]
                )

            else:
                raise ProtocolError(
                    f"Неизвестная команда: {command}"
                )

        logger.info("Выполнена команда: %s", command)

        return {
            "status": "success",
            "data": result
        }

    except KeyError as error:
        return {
            "status": "error",
            "error": f"Отсутствует поле: {error.args[0]}"
        }

    except (InsuranceError, ValueError, TypeError) as error:
        logger.warning("Ошибка запроса: %s", error)

        return {
            "status": "error",
            "error": str(error)
        }


def handle_client(
    client_socket: socket.socket,
    address: tuple
) -> None:
    """Обслуживает отдельного TCP-клиента."""
    logger.info("Подключился клиент: %s", address)

    try:
        with client_socket:
            client_socket.settimeout(CLIENT_TIMEOUT)

            while True:
                try:
                    request = receive_message(client_socket)
                    response = process_request(request)
                    send_message(client_socket, response)

                except socket.timeout:
                    logger.warning(
                        "Тайм-аут клиента: %s",
                        address
                    )
                    break

                except ProtocolError as error:
                    if str(error) != "Соединение закрыто":
                        logger.warning(
                            "Ошибка протокола от %s: %s",
                            address,
                            error
                        )
                    break

                except OSError as error:
                    logger.warning(
                        "Ошибка соединения %s: %s",
                        address,
                        error
                    )
                    break

    finally:
        logger.info("Клиент отключился: %s", address)


def start_server() -> None:
    """Запускает многопоточный TCP-сервер."""
    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as server_socket:

        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        server_socket.bind((HOST, PORT))
        server_socket.listen()

        logger.info(
            "Сервер запущен на %s:%s",
            HOST,
            PORT
        )

        try:
            while True:
                client_socket, address = server_socket.accept()

                thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, address),
                    daemon=True
                )

                thread.start()

        except KeyboardInterrupt:
            logger.info("Сервер остановлен")


if __name__ == "__main__":
    start_server()
