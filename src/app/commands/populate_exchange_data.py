import logging

from app.clients.binance.binance_client import BinanceClient
from app.clients.client_exception import ClientException
from app.services import DatabaseService
from app.services.exchanges.binance_exchange_service import BinanceExchangeService
from app.services.setup_service import SetupService


def show_help():
    return """
    Populates the initial exchange data.
    
    Usage:
    python manage.py populate_exchange_data
"""


def execute(arguments: list):
    logging.info("Populating Binance exchange data")
    populate_binance_data()
    logging.info("Finished populating Binance exchange data")


def populate_binance_data():
    with DatabaseService.create_session() as session:
        service = BinanceExchangeService(session)
        exchange = service.refresh_exchange()

        SetupService.setUpExchange(session=session, exchange_code=exchange.code)
