from abc import ABC, abstractmethod


class ClientBase(ABC):
    fetching_symbols = []

    @abstractmethod
    def get_candles(self, symbol: str, start: int = None, end: int = None, interval: str = "1m") -> list:
        """Retrieve a list of candles for a given symbol, filtering by period.
        Each candle should contain the following params:
            - timestamp
            - open
            - high
            - low
            - close
            - volume"""
        raise NotImplementedError

    @abstractmethod
    def get_symbols(self) -> list:
        """Retrieve a list of all available symbols.
        Each symbol should contain the following params:
            - symbol
            - currencyBase
            - currencyQuote"""
        raise NotImplementedError
