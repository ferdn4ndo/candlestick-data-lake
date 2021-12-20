from datetime import datetime
from binance import AsyncClient, BinanceSocketManager
from app.services import DatabaseService
from app.services.exchanges.binance_exchange_service import BinanceExchangeService


class BinanceWebsocket:
    def __init__(self):
        session = DatabaseService.create_session()
        self.service = BinanceExchangeService(session)
        self.manager = None
        pass

    async def get_manager(self):
        if self.manager is None:
            client = await AsyncClient.create()
            self.manager = BinanceSocketManager(client)

        return self.manager

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
        manager = await self.get_manager()

        ts = manager.multiplex_socket(
            [
                "btcusdt@kline_1m",
                "ethusdt@kline_1m",
            ]
        )

        async with ts as tscm:
            while True:
                res = await tscm.recv()
                print(res)
                await self.handle_message(res)

    async def handle_message(self, res):
        symbol = res["data"]["k"]["s"]
        timestamp = int(res["data"]["E"] / 1000)
        open = res["data"]["k"]["o"]
        close = res["data"]["k"]["c"]
        high = res["data"]["k"]["h"]
        low = res["data"]["k"]["l"]
        volume = res["data"]["k"]["v"]
        closed = res["data"]["k"]["x"]

        fomratted_timestamp = datetime.fromtimestamp(res["data"]["E"] / 1000)
        formatted_start = datetime.fromtimestamp(res["data"]["k"]["t"] / 1000)
        formatter_end = datetime.fromtimestamp(res["data"]["k"]["T"] / 1000)
        print(
            "timestamp: {} | start: {} | end: {} | open: {} | close: {} | high: {} | low: {} | volume: {} | closed: {}".format(
                fomratted_timestamp, formatted_start, formatter_end, open, close, high, low, volume, closed
            )
        )

        if closed is True:
            await self.save_candlestick(symbol, timestamp, open, high, low, close, volume)

    async def save_candlestick(
        self, symbol: str, timestamp: int, open: float, high: float, low: float, close: float, volume: float
    ) -> None:
        pair = self.service.get_currency_pair(BinanceExchangeService.EXCHANGE_CODE, symbol)
        self.service.add_candlestick(
            pair, {"timestamp": timestamp, "open": open, "high": high, "low": low, "close": close, "volume": volume}
        )

        self.service.database.session.commit()
