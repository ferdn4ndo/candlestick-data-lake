import logging

from app import binance_websocket_service


def show_help() -> str:
    return """
    Manage the Binance websocket service

    Usage:
    python manage.py manage_binance_websocket_service OPERATION PAIR1 [PAIR2] [PAIR3] ...
"""


def execute(arguments: list) -> None:
    operation = arguments[1]
    pairs = arguments[2:]

    if operation == "add_pair":
        binance_websocket_service.register_pair(pairs)
    else:
        print(f"The operation '{operation}' is not supported!")


def add_websocket_pairs(pairs: list) -> None:
    for pair in pairs:
        logging.info("Registering pair {}".format(pair))
        binance_websocket_service.register_pair(pair)
