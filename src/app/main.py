import tornado.ioloop
import tornado.web
from binance import AsyncClient, BinanceSocketManager

from app import APP_PORT, DEVELOPMENT_MODE, STATIC_PATH
from app.clients.binance.binance_client import BinanceClient
from app.router import routes
from app.services import DatabaseService
from app.services.consumer_service import ConsumerService
from app.services.exchanges.binance_exchange_service import BinanceExchangeService


def make_app():
    if DEVELOPMENT_MODE:
        print("Starting in DEBUG/DEVELOPMENT mode at port {}".format(APP_PORT))

    return tornado.web.Application(
        routes,
        db=DatabaseService.get_db(),
        debug=DEVELOPMENT_MODE,
        static_path=STATIC_PATH,
    )


async def init_websocket():
    """
    Instantiate socket manager and start loop
    """
    # inicializa um 'multiplex socket': https://python-binance.readthedocs.io/en/latest/websockets.html#id1
    client = await AsyncClient.create()
    socket_manager = BinanceSocketManager(client)

    # Inicializa vazio, e registra aqui quando o par for 'inicializado'
    multiplex_socket = socket_manager.multiplex_socket([])
    socket_manager.kline_socket()

    # TODO como inicializar o loop?


if __name__ == "__main__":
    init_exchanges()
    tornado_app = make_app()
    tornado_app.listen(APP_PORT)

    loop = tornado.ioloop.IOLoop.current()
    loop.add_handler
    loop.start()
