import json
import socket

import pytest

from protocol import (
    send_message,
    receive_message,
    MAX_MESSAGE_SIZE
)
from exceptions import ProtocolError


@pytest.fixture
def sockets():
    client, server = socket.socketpair()

    try:
        yield client, server
    finally:
        client.close()
        server.close()


def test_send_message(sockets):
    client, server = sockets

    data = {
        "command": "get_policy",
        "policy_id": 1
    }

    send_message(client, data)

    received = server.recv(1024)
    result = json.loads(received.decode("utf-8"))

    assert result == data
    assert received.endswith(b"\n")


def test_receive_message(sockets):
    client, server = sockets

    data = {
        "command": "get_all_policies"
    }

    message = json.dumps(data).encode("utf-8") + b"\n"
    client.sendall(message)

    result = receive_message(server)

    assert result == data


def test_send_and_receive_message(sockets):
    client, server = sockets

    data = {
        "status": "success",
        "data": {
            "id": 1,
            "client_name": "Иван Иванов"
        }
    }

    send_message(client, data)
    result = receive_message(server)

    assert result == data


def test_unicode_message(sockets):
    client, server = sockets

    data = {
        "client_name": "Иван Иванов",
        "insurance_type": "Авто"
    }

    send_message(client, data)
    result = receive_message(server)

    assert result == data


def test_multiple_messages(sockets):
    client, server = sockets

    first = {"command": "get_policy", "policy_id": 1}
    second = {"command": "get_policy", "policy_id": 2}

    send_message(client, first)
    send_message(client, second)

    assert receive_message(server) == first
    assert receive_message(server) == second


def test_invalid_json(sockets):
    client, server = sockets

    client.sendall(b"{invalid json}\n")

    with pytest.raises(ProtocolError):
        receive_message(server)


def test_json_not_object(sockets):
    client, server = sockets

    client.sendall(b"[1, 2, 3]\n")

    with pytest.raises(ProtocolError):
        receive_message(server)


def test_invalid_utf8(sockets):
    client, server = sockets

    client.sendall(b"\xff\xfe\n")

    with pytest.raises(ProtocolError):
        receive_message(server)


def test_closed_connection(sockets):
    client, server = sockets

    client.close()

    with pytest.raises(ProtocolError):
        receive_message(server)


def test_send_invalid_data(sockets):
    client, server = sockets

    data = {"values": {1, 2, 3}}

    with pytest.raises(ProtocolError):
        send_message(client, data)


def test_send_oversized_message(sockets):
    client, server = sockets

    data = {
        "message": "A" * MAX_MESSAGE_SIZE
    }

    with pytest.raises(ProtocolError):
        send_message(client, data)



def test_receive_oversized_message(sockets):
    client, server = sockets

    import threading

    def send_large_message():
        try:
            client.sendall(b"A" * (MAX_MESSAGE_SIZE + 1))
        except OSError:
            pass

    thread = threading.Thread(
        target=send_large_message,
        daemon=True
    )
    thread.start()

    with pytest.raises(ProtocolError):
        receive_message(server)

    thread.join(timeout=2)
