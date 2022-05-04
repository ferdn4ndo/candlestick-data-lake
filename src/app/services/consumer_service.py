import asyncio
import datetime
import functools
import logging

from sqlalchemy.orm import Session
from tornado import gen

from app.clients.client_base import ClientBase
from app.clients.client_exception import ClientException
from app.errors import ResourceAlreadyInUseError, ClientIntegrationError
from app.models import CurrencyPair, Exchange
from app.services.currency_pair.currency_pair_factory import get_exchange_currency_pair_from_symbol
from app.services.currency_pair.currency_pair_service import CurrencyPairService
from app.services.database_service import DatabaseService
from app.services.exchanges.exchange_service_base import ExchangeServiceBase
from app.services.exchanges.exchange_service_factory import create_exchange_service_from_code


class ConsumerService:
    AGENT_NAME = "CONSUMER_SERVICE"

    def __init__(self, session: Session, exchange: Exchange, client: ClientBase, service: ExchangeServiceBase) -> None:
        self.client = client
        self.session = session
        self.service = service
        self.exchange = exchange
        self.currency_pairs_in_use = []

    def populate_exchange_data(self) -> None:
        try:
            symbols = self.client.get_symbols()
        except ClientException:
            # TODO [feature-5] Handle possible exceptions. For example: timeout, throttling, IP Ban
            raise ClientIntegrationError(f"Error while getting symbols for exchange '{self.exchange.code}'")

        for symbol in symbols:
            currency_base = self.service.add_currency(symbol["currencyBase"])
            currency_quote = self.service.add_currency(symbol["currencyQuote"])

            self.service.add_currency_pair(self.exchange, symbol["symbol"], currency_base, currency_quote)

            self.session.commit()

    @staticmethod
    def populate_candlesticks(
        client: ClientBase, service: ExchangeServiceBase, exchange_code: str, pair_symbol: str
    ) -> None:
        logging.info(
            "Starting populating historical candlesticks from {} for symbol {}".format(exchange_code, pair_symbol)
        )

        def print_timestamp(timestamp):
            if timestamp is None:
                return "--Newest--"

            return datetime.datetime.fromtimestamp(float(timestamp)).isoformat()

        last_timestamp = None
        while CurrencyPairService.is_in_use(pair_symbol=pair_symbol, exchange_code=exchange_code, agent=ConsumerService.AGENT_NAME):
            logging.info(
                "Getting candles for symbol {} from exchange {} starting from {}".format(
                    pair_symbol,
                    exchange_code,
                    print_timestamp(last_timestamp),
                )
            )

            try:
                candles = client.get_candles(symbol=pair_symbol, end=last_timestamp)
            except ClientException:
                # TODO [feature-5] Handle possible exceptions. For example: timeout, throttling, IP Ban
                raise Exception("Unable to execute the get_candles method for the timestamp {}".format(last_timestamp))

            if not candles or (last_timestamp is not None and last_timestamp == candles[0]["timestamp"]):
                # Reached the end of available candles
                break

            with DatabaseService.create_session() as session:
                exchange = session.query(Exchange).filter_by(code=exchange_code).one()
                currency_pair = session.query(CurrencyPair).filter_by(exchange=exchange, symbol=pair_symbol).one()

                for candle in candles:
                    service.add_candlestick(session=session, pair=currency_pair, candle_data=candle)

                session.commit()

            last_timestamp = candles[0]["timestamp"]

    @staticmethod
    def fetch_currency_pair_candles_in_background(
        client: ClientBase,
        service: ExchangeServiceBase,
        exchange_code: str,
        pair_symbol: str,
    ):
        logging.info(
            "Entering background candle fetching from exchange '{}' and currency pair '{}'".format(
                exchange_code,
                pair_symbol,
            )
        )

        ConsumerService.populate_candlesticks(
            client=client,
            service=service,
            exchange_code=exchange_code,
            pair_symbol=pair_symbol,
        )
        
        in_use = CurrencyPairService.check_in_use(
            pair_symbol=pair_symbol,
            exchange_code=exchange_code,
            agent=ConsumerService.AGENT_NAME,
        )
        if in_use:
            CurrencyPairService.reset_in_use(
                pair_symbol=pair_symbol,
                exchange_code=exchange_code,
                agent=ConsumerService.AGENT_NAME,
                raise_error=False,
            )
        else:
            logging.info("Background candle fetching already stopped from manual action")
