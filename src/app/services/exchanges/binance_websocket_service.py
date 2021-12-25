import asyncio

from datetime import datetime
from binance import AsyncClient, BinanceSocketManager
from app.services import DatabaseService
from app.services.exchanges.binance_exchange_service import BinanceExchangeService


class BinanceWebsocketService:
    def __init__(self):
        session = DatabaseService.create_session()
        self.service = BinanceExchangeService(session)
        self.loop = asyncio.get_event_loop()
        self.pairs = []
        self.manager = None

    async def get_manager(self) -> BinanceSocketManager:
        if self.manager is None:
            client = await AsyncClient.create()
            self.manager = BinanceSocketManager(client)

        return self.manager

    def register_pair(self, symbol) -> None:
        self.pairs.append(symbol)

    def unregister_pair(self, symbol) -> None:
        self.pairs.remove(symbol)

    def restart(self) -> None:
        self.loop.stop()
        self.listen()

    def listen(self) -> None:
        self.loop.run_until_complete(self.process())

    async def process(self) -> None:
        manager = await self.get_manager()

        ts = manager.multiplex_socket(self._get_multiplex_socket_value())

        async with ts as tscm:
            while True:
                res = await tscm.recv()
                await self.handle_message(res)

    async def handle_message(self, res: dict) -> None:
        symbol = res["data"]["k"]["s"]
        timestamp = int(res["data"]["E"] / 1000)
        open = res["data"]["k"]["o"]
        close = res["data"]["k"]["c"]
        high = res["data"]["k"]["h"]
        low = res["data"]["k"]["l"]
        volume = res["data"]["k"]["v"]
        closed = res["data"]["k"]["x"]

        if closed is True:
            fomratted_timestamp = datetime.fromtimestamp(res["data"]["E"] / 1000)
            formatted_start = datetime.fromtimestamp(res["data"]["k"]["t"] / 1000)
            formatter_end = datetime.fromtimestamp(res["data"]["k"]["T"] / 1000)
            print(
                "timestamp: {} | symbol: {} | start: {} | end: {} | open: {} | close: {} | high: {} | low: {} | volume: {} | closed: {}".format(
                    fomratted_timestamp, symbol, formatted_start, formatter_end, open, close, high, low, volume, closed
                )
            )

            await self.save_candlestick(symbol, timestamp, open, high, low, close, volume)

    async def save_candlestick(
        self, symbol: str, timestamp: int, open: float, high: float, low: float, close: float, volume: float
    ) -> None:
        pair = self.service.get_currency_pair(BinanceExchangeService.EXCHANGE_CODE, symbol)
        self.service.add_candlestick(
            pair, {"timestamp": timestamp, "open": open, "high": high, "low": low, "close": close, "volume": volume}
        )

        self.service.database.session.commit()

    def _get_multiplex_socket_value(self) -> list:
        sockets = []
        for pair in self.pairs:
            sockets.append("{}@kline_1m".format(pair.lower()))

        return sockets
