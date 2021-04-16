import os
from datetime import datetime

from app.models import Candlestick, Currency, CurrencyPair, Exchange
from app.services.exchanges.exchange_service_base import ExchangeServiceBase


class BinanceExchangeService(ExchangeServiceBase):
    EXCHANGE_CODE = "binance"
    EXCHANGE_NAME = "Binance Exchange"
