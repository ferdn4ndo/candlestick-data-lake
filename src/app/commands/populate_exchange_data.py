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
    print("Populating Binance exchange data")
    populate_binance_data()


def populate_binance_data():
    session = DatabaseService.create_session()

    client = BinanceClient()
    service = BinanceExchangeService(session)
    exchange = service.refresh_exchange()

    try:
        symbols = client.get_symbols()
    except ClientException as ex:
        print("Exchange exception")
        print(ex)
        # TODO [feature-5] Handle possible exceptions. For example: timeout, throttling, IP Ban
        return

    for symbol in symbols:
        currency_base = service.add_currency(symbol["currencyBase"])
        currency_quote = service.add_currency(symbol["currencyQuote"])

        service.add_currency_pair(exchange, symbol["symbol"], currency_base, currency_quote)

    service.database.session.commit()
