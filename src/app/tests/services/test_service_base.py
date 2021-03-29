import unittest
from unittest.mock import patch
from services.service_base import ServiceBase


class TestServiceBase(unittest.TestCase):
    @patch("services.service_base.ServiceBase.__abstractmethods__", set())
    def setUp(self):
        self.service = ServiceBase()

    def test_init_exchange(self) -> None:
        self.assertRaises(NotImplementedError, self.service.init_exchange)

    def test_populate_candlesticks(self) -> None:
        self.assertRaises(NotImplementedError, self.service.populate_candlesticks, 'BTCUSDT')
