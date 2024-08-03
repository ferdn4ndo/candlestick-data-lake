import requests

from app.clients.client_exception import ClientException
from app.clients.client_base import ClientBase


class BinanceClient(ClientBase):
    URL_BASE = "https://api.binance.com/api/v3"  # https://binance-docs.github.io/apidocs/spot/en/

    PATH_EXCHANGE_INFO = "/exchangeInfo"  # https://binance-docs.github.io/apidocs/spot/en/#exchange-information
    PATH_KLINES = "/klines"  # https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data

    def get_candles(self, symbol: str, start: int = None, end: int = None, interval: str = "1m") -> list:
        params = {"symbol": symbol, "interval": interval, "limit": 1000}
        if start:
            params["startTime"] = start * 1000  # to miliseconds
        if end:
            params["endTime"] = end * 1000  # to miliseconds

        try:
            response = requests.get("{}{}".format(self.URL_BASE, self.PATH_KLINES), params)
        except Exception:
            # TODO [feature-5] Improve it
            raise ClientException

        self._check_response(response)

        candles = response.json()

        formatted_candles = []
        for candle in candles:
            formatted_candles.append(
                {
                    "timestamp": int(candle[0] / 1000),
                    "open": float(candle[1]),
                    "high": float(candle[2]),
                    "low": float(candle[3]),
                    "close": float(candle[4]),
                    "volume": float(candle[5]),
                }
            )

        return formatted_candles

    def get_symbols(self) -> list:
        try:
            response = requests.get("{}{}".format(self.URL_BASE, self.PATH_EXCHANGE_INFO))
        except Exception:
            # TODO [feature-5] Improve it
            raise ClientException
        else:
            self._check_response(response)

        info = response.json()

        formatted_symbols = []
        for symbol in info["symbols"]:
            formatted_symbols.append(
                {
                    "symbol": symbol["symbol"],
                    "currencyBase": symbol["baseAsset"],
                    "currencyQuote": symbol["quoteAsset"],
                }
            )

        return formatted_symbols

    def _check_response(self, response: requests.Response) -> None:
        # TODO [feature-5] Improve it
        if response.status_code != requests.codes.ok:
            raise ClientException
