import unittest

from sqlalchemy.orm import Session
from unittest.mock import patch

from app.models import Currency, CurrencyPair, Exchange
from app.services.exchanges.exchange_service_base import ExchangeServiceBase


class TestExchangeServiceBase(unittest.TestCase):
    @patch("app.services.exchanges.exchange_service_base.ExchangeServiceBase.__abstractmethods__", set())
    def setUp(self):
        self.session = Session()
        self.service = ExchangeServiceBase(self.session)

    def test__init__(self) -> None:
        self.assertEqual(self.session, self.service.session)

    def test_add_exchange(self) -> None:
        self.assertRaises(NotImplementedError, self.service.add_exchange)

    def test_add_currency(self) -> None:
        self.assertRaises(NotImplementedError, self.service.add_currency, "BTCUSDT")

    def test_add_currency_pair(self) -> None:
        self.assertRaises(
            NotImplementedError,
            self.service.add_currency_pair,
            "BTCUSDT",
            Exchange(),
            Currency(),
            Currency(),
        )

    def test_add_candlestick(self) -> None:
        self.assertRaises(NotImplementedError, self.service.add_candlestick, "BTCUSDT", CurrencyPair())
