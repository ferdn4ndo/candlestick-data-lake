from app.clients.binance.binance_websocket import BinanceWebsocket


def show_help():
    return """
    Start Binance websocket consumption.

    Usage:
    python manage.py init_binance_websocket
"""


def execute(arguments: list):
    print("Starting Binance websocket")
    start_binance_websocket()


def start_binance_websocket():
    websocket = BinanceWebsocket()
    # recebe lista de pares
    websocket.register_pair("BTCUSDT")
    websocket.register_pair("ETHUSDT")
    websocket.listen()
