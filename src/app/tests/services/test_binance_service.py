from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_get_or_create import update_or_create
import unittest
from unittest.mock import patch, MagicMock

from services.binance_service import BinanceService
from models import Exchange, Currency, CurrencyPair, Candlestick


class TestBinanceService(unittest.TestCase):

    @patch('services.binance_service.BinanceService._create_db_session')
    def setUp(self, mock_create_db_session: MagicMock) -> None:
        mock_create_db_session.return_value = Session()
        self.service = BinanceService()

    def test_init_exchange(self) -> None:
        pass

    def test_populate_candlesticks(self) -> None:
        pass

    def test_populate_currency_pair(self) -> None:
        pass

    @patch('sqlalchemy_get_or_create.update_or_create')
    def test_add_exchange(self, mock_update_or_create: MagicMock) -> None:
        exchange = Exchange()
        mock_update_or_create.return_value = (exchange, True)

        response = self.service.add_exchange()

        mock_update_or_create.assert_called_once_with(
            self.service._session,
            Exchange,
            code='binance',
            defaults={'name': 'Binance Exchange'}
        )
        self.assertEqual(exchange, response)

    @patch('sqlalchemy_get_or_create.update_or_create')
    def test_add_currency(self, mock_update_or_create: MagicMock) -> None:
        currency = Currency()
        mock_update_or_create.return_value = (currency, True)

        response = self.service.add_currency('BTCUSDT')

        mock_update_or_create.assert_called_once_with(
            self.service._session,
            Currency,
            symbol='BTCUSDT',
            defaults={'name': 'BTCUSDT'}
        )
        self.assertEqual(currency, response)

    @patch('sqlalchemy_get_or_create.update_or_create')
    def test_add_currency_pair(self, mock_update_or_create: MagicMock) -> None:
        exchange = Exchange()
        currency_pair = CurrencyPair()
        mock_update_or_create.return_value = (currency_pair, True)

        currency_base = Currency()
        currency_quote = Currency()
        response = self.service.add_currency_pair(exchange, 'BTCUSDT', currency_base, currency_quote)

        mock_update_or_create.assert_called_once_with(
            self.service._session,
            CurrencyPair,
            exchange=exchange,
            symbol='BTCUSDT',
            defaults={'currency_base': currency_base, 'currency_quote': currency_quote}
        )

        self.assertEqual(currency_pair, response)

    @patch('sqlalchemy_get_or_create.update_or_create')
    def test_add_candlestick(self, mock_update_or_create: MagicMock) -> None:
        candlestick = Candlestick()
        mock_update_or_create.return_value = (candlestick, True)

        currency_pair = CurrencyPair()
        response = self.service.add_candlestick(
            currency_pair,
            {'timestamp': 1231006505, 'open': 100.0, 'high': 200.0, 'low': 50.0, 'close': 150, 'volume': 420.69}
        )

        mock_update_or_create.assert_called_once_with(
            self.service._session,
            Candlestick,
            currency_pair=currency_pair,
            timestamp=1231006505,
            defaults={
                'open': 100.0,
                'high': 200.0,
                'low': 50.0,
                'close': 150.0,
                'volume': 420.69,
            }
        )
        self.assertEqual(candlestick, response)