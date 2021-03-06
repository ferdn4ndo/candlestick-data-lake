import os
from abc import ABC
from datetime import datetime

from app.models import Currency, CurrencyPair, Exchange
from app.services.database_service import DatabaseService
import sqlalchemy_get_or_create
from app.models import Candlestick, Currency, CurrencyPair, Exchange
from sqlalchemy.orm import Session


class ExchangeServiceBase(ABC):
    EXCHANGE_CODE = None
    EXCHANGE_NAME = None

    def __init__(self, session: Session) -> None:
        self.database = DatabaseService(session)

    def add_exchange(self) -> Exchange:
        (exchange, _) = self.database.update_or_create(
            Exchange,
            code=self.EXCHANGE_CODE,
            defaults={"name": self.EXCHANGE_NAME},
        )

        return exchange

    def add_currency(self, symbol: str) -> Currency:
        (currency, _) = self.database.update_or_create(Currency, symbol=symbol, defaults={"name": symbol})

        return currency

    def add_currency_pair(
        self,
        exchange: Exchange,
        symbol: str,
        currency_base: Currency,
        currency_quote: Currency,
    ) -> CurrencyPair:
        (currency_pair, _) = self.database.update_or_create(
            CurrencyPair,
            exchange=exchange,
            symbol=symbol,
            defaults={"currency_base": currency_base, "currency_quote": currency_quote},
        )

        return currency_pair

    def add_candlestick(self, pair: CurrencyPair, candle_data: list) -> None:
        (candlestick, _) = self.database.update_or_create(
            Candlestick,
            currency_pair=pair,
            timestamp=candle_data["timestamp"],
            defaults={
                "open": candle_data["open"],
                "high": candle_data["high"],
                "low": candle_data["low"],
                "close": candle_data["close"],
                "volume": candle_data["volume"],
            },
        )

        return candlestick
