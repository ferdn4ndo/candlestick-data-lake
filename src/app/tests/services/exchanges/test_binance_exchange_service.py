import unittest

from app.services.exchanges.binance_exchange_service import BinanceExchangeService
from sqlalchemy.orm import Session


class TestBinanceExchangeService(unittest.TestCase):
    def setUp(self) -> None:
        self.service = BinanceExchangeService(Session())

    def test_constants(self) -> None:
        self.assertEqual(self.service.EXCHANGE_CODE, "binance")
        self.assertEqual(self.service.EXCHANGE_NAME, "Binance Exchange")
