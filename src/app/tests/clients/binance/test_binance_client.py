import requests
import unittest
from unittest.mock import patch, MagicMock

from clients.binance.binance_client import BinanceClient


class TestBinanceClient(unittest.TestCase):

    def setUp(self) -> None:
        self.client = BinanceClient()

    @patch('requests.get')
    def test_get_candles_success(self, mock_get: MagicMock) -> None:
        json_data = [
            [1616958060000, '55245.09000000', '55288.22000000', '55210.00000000', '55246.24000000', '37.85910100'],
            [1616958120000, '55247.32000000', '55257.09000000', '55155.16000000', '55181.40000000', '39.21859600'],
        ]
        mock_get.return_value = self.create_mock_response(200, json_data)

        response = self.client.get_candles('BTCUSDT', 1616958000, 1616961720)

        mock_get.assert_called_once_with(
            'https://api.binance.com/api/v3/klines',
            {'symbol': 'BTCUSDT', 'interval': '1m', 'limit': 1000, 'startTime': 1616958000, 'endTime': 1616961720}
        )

        expected = [
            {
                'timestamp': 1616958060,
                'open': 55245.09,
                'high': 55288.22,
                'low': 55210,
                'close': 55246.24,
                'volume': 37.859101,
            },
            {
                'timestamp': 1616958120,
                'open': 55247.32,
                'high': 55257.09,
                'low': 55155.16,
                'close': 55181.4,
                'volume': 39.218596,
            }
        ]
        self.assertListEqual(expected, response)

    @patch('requests.get')
    def test_get_symbols_success(self, mock_get: MagicMock) -> None:
        json_data = {
            'symbols': [
                {'symbol': 'BTCUSDT', 'baseAsset': 'BTC', 'quoteAsset': 'USDT'},
                {'symbol': 'BNBBTC', 'baseAsset': 'BNB', 'quoteAsset': 'BTC'},
            ]
        }
        mock_get.return_value = self.create_mock_response(200, json_data)

        response = self.client.get_symbols()

        mock_get.assert_called_once_with('https://api.binance.com/api/v3/exchangeInfo')

        expected = [
            {'symbol': 'BTCUSDT', 'currencyBase': 'BTC', 'currencyQuote': 'USDT'},
            {'symbol': 'BNBBTC', 'currencyBase': 'BNB', 'currencyQuote': 'BTC'},
        ]
        self.assertListEqual(expected, response)

    def create_mock_response(self, status_code: int = 200, json_data: str = None) -> MagicMock:
        mock = MagicMock(status_code=status_code)

        if json_data is not None:
            attrs = {'json.return_value': json_data}
            mock.configure_mock(**attrs)

        return mock


if __name__ == '__main__':
    unittest.main()
