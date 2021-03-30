from abc import ABC, abstractmethod

from models import Currency, CurrencyPair, Exchange
from sqlalchemy.orm import Session


class ExchangeServiceBase(ABC):
    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    def add_exchange(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_currency(self, symbol: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_currency_pair(self, exchange: Exchange, symbol: str, currency_base: Currency, currency_quote: Currency) -> CurrencyPair:
        raise NotImplementedError

    @abstractmethod
    def add_candlestick(self, pair: CurrencyPair, candle_data: list) -> None:
        raise NotImplementedError
