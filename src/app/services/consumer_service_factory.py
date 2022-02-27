from sqlalchemy.orm import Session

from app.clients.binance.binance_client import BinanceClient
from app.clients.client_base import ClientBase
from app.errors import UnsupportedTypeError
from app.models import Exchange
from app.services.consumer_service import ConsumerService
from app.services.exchanges.binance_exchange_service import BinanceExchangeService
from app.services.exchanges.exchange_service_base import ExchangeServiceBase


def create_consumer_service_from_exchange(session: Session, exchange: Exchange) -> ConsumerService:
    if exchange.code == BinanceExchangeService.EXCHANGE_CODE:
        client = BinanceClient()
        service = BinanceExchangeService()

        return ConsumerService(session=session, exchange=exchange, client=client, service=service)

    raise UnsupportedTypeError(f"The exchange code '{exchange.code}' is not supported.")


def create_client_from_exchange_code(exchange_code: str) -> ClientBase:
    if exchange_code == BinanceExchangeService.EXCHANGE_CODE:
        return BinanceClient()

    raise UnsupportedTypeError(f"The exchange code '{exchange_code}' is not supported.")


def create_service_from_exchange_code(exchange_code: str) -> ExchangeServiceBase:
    if exchange_code == BinanceExchangeService.EXCHANGE_CODE:
        return BinanceExchangeService()

    raise UnsupportedTypeError(f"The exchange code '{exchange_code}' is not supported.")
