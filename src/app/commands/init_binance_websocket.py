import sys
from app.services.exchanges.binance_websocket_service import BinanceWebsocketService


def show_help():
    return """
    Start Binance websocket consumption.

    Usage:
    python manage.py init_binance_websocket
"""


def execute(arguments: list):
    pairs = sys.argv[1:]

    print("Starting Binance websocket for:")
    print(*pairs, sep=", ")

    start_binance_websocket(pairs)


def start_binance_websocket(pairs):
    service = BinanceWebsocketService()

    for pair in pairs:
        service.register_pair(pair)

    service.listen()
