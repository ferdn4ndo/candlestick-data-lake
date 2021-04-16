import unittest

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_get_or_create import update_or_create
from unittest.mock import patch, MagicMock

from app.services.exchanges.binance_exchange_service import BinanceExchangeService
from app.models import Exchange, Currency, CurrencyPair, Candlestick


class TestBinanceExchangeService(unittest.TestCase):
    def setUp(self) -> None:
        self.service = BinanceExchangeService(Session())

    def test_constants(self) -> None:
        self.assertEqual(self.service.EXCHANGE_CODE, "binance")
        self.assertEqual(self.service.EXCHANGE_NAME, "Binance Exchange")
