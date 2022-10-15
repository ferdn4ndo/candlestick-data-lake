import logging
from abc import ABC

from sqlalchemy.orm import Session

from app.models import Candlestick, Currency, CurrencyPair, Exchange
from app.services.database_service import DatabaseService


class ExchangeServiceBase(ABC):
    EXCHANGE_CODE = None
    EXCHANGE_NAME = None

    def __init__(self, exchange: Exchange = None) -> None:
        self.exchange = exchange

    def add_exchange(self) -> Exchange:
        logging.info(f"Creating exchange using code '{self.EXCHANGE_CODE}'")

        with DatabaseService.create_session() as session:
            database_service = DatabaseService(session)
            exchange = database_service.create(
                Exchange,
                code=self.EXCHANGE_CODE,
                defaults={"name": self.EXCHANGE_NAME},
            )

            session.commit()

        self.exchange = exchange

        return exchange

    def refresh_exchange(self) -> Exchange:
        logging.info(f"Refreshing exchange with code '{self.EXCHANGE_CODE}'")

        with DatabaseService.create_session() as session:
            database_service = DatabaseService(session)
            self.exchange = database_service.find_or_create(
                Exchange,
                code=self.EXCHANGE_CODE,
                defaults={"name": self.EXCHANGE_NAME},
            )

        return self.exchange

    def add_currency(self, symbol: str) -> Currency:
        with DatabaseService.create_session() as session:
            database_service = DatabaseService(session)
            currency = database_service.find_or_create(Currency, symbol=symbol, defaults={"name": symbol})

        return currency

    def add_currency_pair(
        self,
        session: Session,
        exchange: Exchange,
        symbol: str,
        currency_base: Currency,
        currency_quote: Currency,
    ) -> CurrencyPair:
        database_service = DatabaseService(session)
        currency_pair = database_service.find_or_create(
            CurrencyPair,
            exchange=exchange,
            symbol=symbol,
            defaults={"currency_base": currency_base, "currency_quote": currency_quote},
        )

        return currency_pair

    def add_candlestick(self, session: Session, pair: CurrencyPair, candle_data: list) -> Candlestick:
        database_service = DatabaseService(session)
        candlestick = database_service.find_or_create(
            Candlestick,
            currency_pair=pair,
            timestamp=candle_data["timestamp"],
            defaults={
                "open": candle_data["open"],
                "high": candle_data["high"],
                "low": candle_data["low"],
                "close": candle_data["close"],
                "volume": candle_data["volume"],
            },
        )

        return candlestick

    def get_currency_pair(self, symbol: str) -> CurrencyPair:
        with DatabaseService.create_session() as session:
            return session.query(CurrencyPair).filter_by(exchange=self.exchange, symbol=symbol).one()

    def list_currency_pairs(self) -> list:
        """
        Returns a list of CurrencyPair objects filtered by the instance's exchange model
        """
        with DatabaseService.create_session() as session:
            return session.query(CurrencyPair).filter_by(exchange=self.exchange).all()

    def list_currency_pairs_symbols(self) -> list:
        """
        Returns a list of symbols (from the CurrencyPair objects) filtered by the instance's exchange model
        """
        currency_pairs = self.list_currency_pairs()

        return [currency_pair.symbol for currency_pair in currency_pairs]

    def serialize_exchange(self) -> dict:
        """
        Serializes an exchange adding the symbols list
        """
        serialized_exchange = self.exchange.serialize()
        serialized_exchange["symbols"] = self.list_currency_pairs_symbols()

        return serialized_exchange
