import logging

from app.clients.binance.binance_client import BinanceClient
from app.clients.client_exception import ClientException
from app.services import DatabaseService
from app.services.exchanges.binance_exchange_service import BinanceExchangeService


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
    session = DatabaseService.create_session()

    client = BinanceClient()
    service = BinanceExchangeService(session)
    exchange = service.refresh_exchange()

    try:
        symbols = client.get_symbols()
    except ClientException as ex:
        logging.error(f"Exchange exception: {ex}")
        # TODO [feature-5] Handle possible exceptions. For example: timeout, throttling, IP Ban
        return

    for symbol in symbols:
        logging.debug(f"Adding symbol {symbol}")
        currency_base = service.add_currency(symbol["currencyBase"])
        currency_quote = service.add_currency(symbol["currencyQuote"])

        service.add_currency_pair(exchange, symbol["symbol"], currency_base, currency_quote)

    session.commit()
