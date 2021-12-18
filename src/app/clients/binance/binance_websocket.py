from datetime import datetime
import asyncio
import json
from binance import AsyncClient, BinanceSocketManager
from app.services import DatabaseService
from app.services.exchanges.binance_exchange_service import BinanceExchangeService
from app.models import Candlestick, Currency, CurrencyPair, Exchange


class BinanceWebsocket:
    def __init__(self):
        session = DatabaseService.create_session()
        self.service = BinanceExchangeService(session)
        pass

    def register_pair(self, symbol):
        pass

    def unregister_pair(self, symbol):
        pass

    def listen(self):
        pass

    async def process(self):
        """{
            "e": "kline",  # event type
            "E": 1499404907056,  # event time
            "s": "ETHBTC",  # symbol
            "k": {
                "t": 1499404860000,  # start time of this bar
                "T": 1499404919999,  # end time of this bar
                "s": "ETHBTC",  # symbol
                "i": "1m",  # interval
                "f": 77462,  # first trade id
                "L": 77465,  # last trade id
                "o": "0.10278577",  # open
                "c": "0.10278645",  # close
                "h": "0.10278712",  # high
                "l": "0.10278518",  # low
                "v": "17.47929838",  # volume
                "n": 4,  # number of trades
                "x": false,  # whether this bar is final
                "q": "1.79662878",  # quote volume
                "V": "2.34879839",        # volume of active buy
                "Q": "0.24142166",        # quote volume of active buy
                "B": "13279784.01349473"  # can be ignored
            }
        }"""
        client = await AsyncClient.create()
        manager = BinanceSocketManager(client)

        # start any sockets here, i.e a trade socket
        ts = manager.kline_socket("BTCUSDT")

        # then start receiving messages
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                await self.handle_message(res)

    async def handle_message(self, res):
        timestamp = datetime.fromtimestamp(res["E"] / 1000)
        start = datetime.fromtimestamp(res["k"]["t"] / 1000)
        end = datetime.fromtimestamp(res["k"]["T"] / 1000)
        open = res["k"]["o"]
        close = res["k"]["c"]
        high = res["k"]["h"]
        low = res["k"]["l"]
        volume = res["k"]["v"]
        closed = res["k"]["x"]

        print(
            "timestamp: {} | start: {} | end: {} | open: {} | close: {} | high: {} | low: {} | volume: {} | closed: {}".format(
                timestamp, start, end, open, close, high, low, volume, closed
            )
        )
        if closed is True:
            await self.save_candlestick(res["E"] / 1000, open, high, low, close, volume)

    async def save_candlestick(self, timestamp, open, high, low, close, volume):
        # recupera exchange
        (exchange, _) = self.service.database.get_or_create(Exchange, code="binance", defaults={"name": "Binance"})

        (currency_a, _) = self.service.database.get_or_create(Currency, symbol="BTC", defaults={"name": "Bitcoin"})
        (currency_b, _) = self.service.database.get_or_create(Currency, symbol="USDT", defaults={"name": "ESD Tether"})
        (pair, _) = self.service.database.get_or_create(
            CurrencyPair,
            exchange=exchange,
            currency_base=currency_a,
            currency_quote=currency_b,
            defaults={"symbol": "BTCUSDT"},
        )

        self.service.add_candlestick(
            pair, {"timestamp": timestamp, "open": open, "high": high, "low": low, "close": close, "volume": volume}
        )

        self.service.database.session.commit()
