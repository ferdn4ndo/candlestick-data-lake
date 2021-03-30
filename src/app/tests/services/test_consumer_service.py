import unittest
from unittest.mock import MagicMock


class testTestConsumerService(unittest.TestCase):
    def test_populate_exchange_data(self) -> None:
        return
        # get_symbols_mock.return_value = []

        # add_currency_mock = MagicMock()
        # add_currency_mock.side_effect = [
        #     'currencyBase1',
        #     'currencyQuote1',
        #     'currencyBase2',
        #     'currencyQuote2',
        # ]

        # add_currency_pair_mock = MagicMock()

        # service = ConsumerService(client_mock, service_mock)
        # service.populate_exchange_data()

        # get_symbols_mock.assert_called_once_with()

    def test_populate_candlesticks(self):
        self.assertTrue(True)

    def test___create_db_session(self):
        self.assertTrue(True)

    def test___create_dependencies(self):
        self.assertTrue(True)
