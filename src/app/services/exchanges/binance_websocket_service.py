import asyncio
import logging
from datetime import datetime

from binance import AsyncClient, BinanceSocketManager

from app.models import CurrencyPair
from app.services.exchanges.binance_exchange_service import BinanceExchangeService


class BinanceWebsocketService:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.pairs = []
        self._manager = None

    async def get_manager(self) -> BinanceSocketManager:
        if self._manager is None:
            client = await AsyncClient.create()
            self._manager = BinanceSocketManager(client)

        return self._manager

    def is_currency_pair_model_registered(self, currency_pair: CurrencyPair) -> bool:
        return self.is_pair_registered(symbol=currency_pair.symbol)

    def is_pair_registered(self, symbol: str) -> bool:
        return symbol in self.pairs

    def register_pair(self, symbol: str) -> None:
        self.pairs.append(symbol)

    def unregister_pair(self, symbol: str) -> None:
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
            logging.info(
                "timestamp: {} | symbol: {} | start: {} | end: {} | open: {} | close: {} | high: {} | low: {} | volume: {} | closed: {}".format(
                    fomratted_timestamp, symbol, formatted_start, formatter_end, open, close, high, low, volume, closed
                )
            )

            await self.save_candlestick(symbol, timestamp, open, high, low, close, volume)

    async def save_candlestick(
        self, symbol: str, timestamp: int, opening: float, high: float, low: float, closing: float, volume: float
    ) -> None:
        global session

        service = BinanceExchangeService(session)
        service.refresh_exchange()

        pair = service.get_currency_pair(symbol)
        service.add_candlestick(
            pair,
            [{"timestamp": timestamp, "open": opening, "high": high, "low": low, "close": closing, "volume": volume}],
        )

        session.commit()

    def _get_multiplex_socket_value(self) -> list:
        sockets = []
        for pair in self.pairs:
            sockets.append("{}@kline_1m".format(pair.lower()))

        return sockets
