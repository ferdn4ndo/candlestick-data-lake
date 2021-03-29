from abc import ABC, abstractmethod
from models import CurrencyPair


class ServiceBase(ABC):

    @abstractmethod
    def init_exchange(self) -> None:
        """Initialize exchange base data:
            - Add exchange entry
            - Add currencies entries
            - Add currencyPairs entries"""
        raise NotImplementedError

    @abstractmethod
    def populate_candlesticks(self, pair: CurrencyPair, timestamp_limit: int = None) -> None:
        """Populate database with historical data for a given CurrencyPair"""
        raise NotImplementedError
