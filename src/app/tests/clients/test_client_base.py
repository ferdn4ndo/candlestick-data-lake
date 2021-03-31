import unittest
from unittest.mock import patch
from clients.client_base import ClientBase


class TestClientBase(unittest.TestCase):
    @patch("clients.client_base.ClientBase.__abstractmethods__", set())
    def setUp(self):
        self.client = ClientBase()

    def test_get_candles(self) -> None:
        self.assertRaises(NotImplementedError, self.client.get_candles, "BTCUSDT")

    def test_get_symbols(self) -> None:
        self.assertRaises(NotImplementedError, self.client.get_symbols)
