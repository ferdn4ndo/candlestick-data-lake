import logging

from app.clients.binance.binance_client import BinanceClient
from app.services import DatabaseService
from app.services.consumer_service import ConsumerService
from app.services.exchanges.binance_exchange_service import BinanceExchangeService
from app.services.exchanges.binance_websocket_service import BinanceWebsocketService
from sqlalchemy.orm import Session


def show_help() -> str:
    return """
    Start Binance websocket consumption.

    Usage:
    python manage.py init_binance_websocket PAIR1 PAIR2 ...
"""


def execute(arguments: list) -> None:
    pairs = arguments[1:]

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    logging.info("Starting Binance for:")
    logging.info(", ".join(pairs))

    session = DatabaseService.create_session()
    populate_binance_data(session)

    # populate_candlesticks(session, pairs)
    start_binance_websocket(session, pairs)


def populate_binance_data(session: Session) -> None:
    client = BinanceClient()
    service = BinanceExchangeService(session)
    consumer = ConsumerService(client, service)

    logging.info("Populating exchange data")
    consumer.populate_exchange_data()


def populate_candlesticks(session: Session, pairs: list) -> None:
    client = BinanceClient()
    service = BinanceExchangeService(session)
    consumer = ConsumerService(client, service)

    for pair in pairs:
        logging.info("Populating candlesticke for {}".format(pair))
        consumer.populate_candlesticks(pair)


def start_binance_websocket(session: Session, pairs: list) -> None:
    service = BinanceWebsocketService(session)

    for pair in pairs:
        logging.info("Registering {}".format(pair))
        service.register_pair(pair)

    service.listen()
