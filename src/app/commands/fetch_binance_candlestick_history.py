import logging

from app.clients.binance.binance_client import BinanceClient
from app.services import DatabaseService
from app.services.consumer_service import ConsumerService
from app.services.exchanges.binance_exchange_service import BinanceExchangeService
from sqlalchemy.orm import Session


def show_help() -> str:
    return """
    Fetches historical candlesticks from Binance.

    Usage:
    python manage.py fetch_binance_candlestick_history PAIR1 PAIR2 ...
"""


def execute(arguments: list) -> None:
    pairs = arguments[1:]

    logging.info(f"Fetching Binance historical candlesticks for pairs: ${', '.join(pairs)}")

    session = DatabaseService.create_session()

    populate_candlesticks(session, pairs)


def populate_candlesticks(session: Session, pairs: list) -> None:
    client = BinanceClient()
    service = BinanceExchangeService(session)
    consumer = ConsumerService(client, service)

    for pair in pairs:
        logging.info(f"Populating candlesticks for pair {pair}")
        consumer.populate_candlesticks(session, BinanceExchangeService.EXCHANGE_CODE, pair)
