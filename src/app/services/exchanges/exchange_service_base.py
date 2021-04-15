from abc import ABC, abstractmethod

from app.models import Currency, CurrencyPair, Exchange
from app.services.database_service import DatabaseService
from sqlalchemy.orm import Session


class ExchangeServiceBase(ABC):
    EXCHANGE_CODE = None

    def __init__(self, session: Session) -> None:
        self.database = DatabaseService(session)

    @abstractmethod
    def add_exchange(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_currency(self, symbol: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_currency_pair(
        self,
        exchange: Exchange,
        symbol: str,
        currency_base: Currency,
        currency_quote: Currency,
    ) -> CurrencyPair:
        raise NotImplementedError

    @abstractmethod
    def add_candlestick(self, pair: CurrencyPair, candle_data: list) -> None:
        raise NotImplementedError
