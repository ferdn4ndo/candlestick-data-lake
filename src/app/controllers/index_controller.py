from app import __version__

from app.controllers.base_controller import BaseController
from app.services.exchanges.binance_exchange_service import BinanceExchangeService
from app.services.consumer_service import ConsumerService
from app.clients.binance.binance_client import BinanceClient


class IndexController(BaseController):
    def get(self):
        client = BinanceClient()
        service = BinanceExchangeService(self.session)

        consumer = ConsumerService(client, service)

        pair_symbol = 'BATUSDT'
        consumer.populate_candlesticks(pair_symbol)

        self.write("CandleStick Data Lake v{}".format(__version__))
