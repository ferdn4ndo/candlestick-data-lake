from sqlalchemy.orm import Session

from app import DatabaseService
from app.errors import InvalidValueError, ResourceNotFoundError
from app.models import Exchange
from app.services.exchanges.binance_exchange_service import BinanceExchangeService
from app.services.exchanges.exchange_service_base import ExchangeServiceBase


ALLOWED_EXCHANGE_CODES = [
    BinanceExchangeService.EXCHANGE_CODE,
]


def get_exchange_by_id(session: Session, exchange_id: int, raise_error: bool = True) -> [Exchange]:
    exchange = session.query(Exchange).filter_by(id = exchange_id).first()

    if raise_error and exchange is None:
        raise ResourceNotFoundError(f"The exchange ID '{exchange_id}' was not found!")

    return exchange


def create_exchange_service_from_model(exchange: Exchange) -> ExchangeServiceBase:
    """
    Returns the correct exchange service from a given exchange model object
    """
    if exchange.code == BinanceExchangeService.EXCHANGE_CODE:
        return BinanceExchangeService(exchange)
    else:
        raise InvalidValueError(f"The exchange code '{exchange.EXCHANGE_CODE}' is not supported.")


def create_exchange_service_from_id(session: Session, exchange_id: int) -> ExchangeServiceBase:
    """
    Returns the correct exchange service from a given exchange model ID
    """

    exchange = session.query(Exchange).filter_by(id = exchange_id).first()

    if exchange is None:
        raise ResourceNotFoundError(f"The exchange ID '{exchange_id}' was not found!")

    return create_exchange_service_from_model(exchange=exchange)


def create_exchange_service_from_code(code: str) -> ExchangeServiceBase:
    """
    Returns the correct exchange service (and its model) from a given exchange code
    """

    if code == BinanceExchangeService.EXCHANGE_CODE:
        return BinanceExchangeService()
    else:
        raise InvalidValueError(f"The exchange code '{code}' is not supported.")


def serialize_existing_exchanges() -> list:
    """
    Returns a list with all the existing exchanges in the database, in a serialized dict
    """
    serialized_exchanges = []

    with DatabaseService.create_session() as session:
        for exchange in session.query(Exchange).order_by(Exchange.id).all():
            service = create_exchange_service_from_model(exchange=exchange)
            serialized_exchanges.append(service.serialize_exchange())

    return serialized_exchanges
