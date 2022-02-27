from sqlalchemy.orm import Session

from app.errors import ResourceNotFoundError
from app.models import CurrencyPair, Exchange


def get_exchange_currency_pair_from_symbol(session: Session, exchange: Exchange, symbol: str) -> CurrencyPair:
    currency_pair = session.query(CurrencyPair).filter_by(exchange=exchange, symbol=symbol).first()

    if currency_pair is None:
        raise ResourceNotFoundError(f"The symbol '{symbol}' was not found in the currency pair list of the '{exchange.code}' exchange!")

    return currency_pair
