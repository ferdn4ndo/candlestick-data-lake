import unittest
from unittest.mock import MagicMock, patch

from app.models import Candlestick, Currency, CurrencyPair, Exchange
from app.services.exchanges.exchange_service_base import ExchangeServiceBase
from sqlalchemy.orm import Session, sessionmaker


class TestExchangeServiceBase(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        self.service = ExchangeServiceBase()

    def test___init__(self) -> None:
        self.assertEqual(self.session, self.service.database.session)

    @patch("app.services.database_service.DatabaseService.update_or_create")
    def test_add_exchange(self, mock_update_or_create: MagicMock) -> None:
        exchange = Exchange()
        mock_update_or_create.return_value = (exchange, True)

        response = self.service.add_exchange()

        mock_update_or_create.assert_called_once_with(
            Exchange,
            code=None,
            defaults={"name": None},
        )
        self.assertEqual(exchange, response)

    @patch("app.services.database_service.DatabaseService.update_or_create")
    def test_add_currency(self, mock_update_or_create: MagicMock) -> None:
        currency = Currency()
        mock_update_or_create.return_value = (currency, True)

        response = self.service.add_currency("BTCUSDT")

        mock_update_or_create.assert_called_once_with(
            Currency,
            symbol="BTCUSDT",
            defaults={"name": "BTCUSDT"},
        )
        self.assertEqual(currency, response)

    @patch("app.services.database_service.DatabaseService.update_or_create")
    def test_add_currency_pair(self, mock_update_or_create: MagicMock) -> None:
        exchange = Exchange()
        currency_pair = CurrencyPair()
        mock_update_or_create.return_value = (currency_pair, True)

        currency_base = Currency()
        currency_quote = Currency()
        response = self.service.add_currency_pair(exchange, "BTCUSDT", currency_base, currency_quote)

        mock_update_or_create.assert_called_once_with(
            CurrencyPair,
            exchange=exchange,
            symbol="BTCUSDT",
            defaults={"currency_base": currency_base, "currency_quote": currency_quote},
        )

        self.assertEqual(currency_pair, response)

    @patch("app.services.database_service.DatabaseService.update_or_create")
    def test_add_candlestick(self, mock_update_or_create: MagicMock) -> None:
        candlestick = Candlestick()
        mock_update_or_create.return_value = (candlestick, True)

        currency_pair = CurrencyPair()
        response = self.service.add_candlestick(
            currency_pair,
            {
                "timestamp": 1231006505,
                "open": 100.0,
                "high": 200.0,
                "low": 50.0,
                "close": 150,
                "volume": 420.69,
            },
        )

        mock_update_or_create.assert_called_once_with(
            Candlestick,
            currency_pair=currency_pair,
            timestamp=1231006505,
            defaults={
                "open": 100.0,
                "high": 200.0,
                "low": 50.0,
                "close": 150.0,
                "volume": 420.69,
            },
        )
        self.assertEqual(candlestick, response)

    @patch("app.services.database_service.DatabaseService.update_or_create")
    def test_get_currency_pair(self, mock_update_or_create: MagicMock) -> None:
        pass
