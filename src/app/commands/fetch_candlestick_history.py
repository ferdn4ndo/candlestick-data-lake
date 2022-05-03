import logging

from app.clients.binance.binance_client import BinanceClient
from app.errors import ResourceNotFoundError, ResourceAlreadyInUseError
from app.services import DatabaseService
from app.services.consumer_service import ConsumerService
from app.services.consumer_service_factory import create_client_from_exchange_code, create_service_from_exchange_code
from app.services.currency_pair.currency_pair_service import CurrencyPairService
from app.services.exchanges.binance_exchange_service import BinanceExchangeService
from sqlalchemy.orm import Session

from app.services.exchanges.exchange_service_factory import get_exchange_by_code


def show_help() -> str:
    return """
    Fetches historical candlesticks.

    Usage:
    python manage.py fetch_binance_candlestick_history <EXCHANGE> <PAIR1> [<PAIR2>] [<PAIR3>] ...
"""


def execute(arguments: list) -> None:
    if len(arguments) < 2:
        logging.error("You must provide at least 2 arguments: <EXCHANGE> and <PAIR1>")
        
    try:
        exchange_code = arguments[1]
        symbol = arguments[2]

        with DatabaseService.create_session() as session:
            exchange = get_exchange_by_code(session=session, exchange_code=exchange_code)
            CurrencyPairService.check_if_symbol_exists(session=session, exchange=exchange, symbol=symbol)
            
            CurrencyPairService.check_in_use(
                agent=ConsumerService.AGENT_NAME,
                exchange_code=exchange.code,
                symbol=symbol,
            )
            
            exchange_client = create_client_from_exchange_code(exchange_code=exchange_code)
            exchange_service = create_service_from_exchange_code(exchange_code=exchange_code)
            
            ConsumerService.fetch_currency_pair_candles_in_background(
                client=exchange_client,
                service=exchange_service,
                exchange_code=exchange_code,
                pair_symbol=symbol,
            )
        
        logging.info(
            f"Finished fetching historical pairs for symbol '{symbol}' from '{exchange_code}'."
        )
    except ResourceNotFoundError as exception:
        logging.error(f"Error when loading resources: {exception}")
    except ResourceAlreadyInUseError as exception:
        logging.error(f"Error when acquiring file lock: {exception}")

    
