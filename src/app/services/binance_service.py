import os

from datetime import datetime
# from sqlalchemy_get_or_create import update_or_create
import sqlalchemy_get_or_create

from models import Candlestick, CurrencyPair, Exchange, Currency
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

from clients.binance.binance_client import BinanceClient
from clients.binance.binance_exception import BinanceException
from services.service_base import ServiceBase


class BinanceService(ServiceBase):

    def __init__(self):
        self.client = BinanceClient()
        self._session = self._create_db_session()

    def init_exchange(self) -> None:
        exchange = self.add_exchange()
        self.populate_currency_pair(exchange)

        self._session.commit()

    def populate_candlesticks(self, pair: CurrencyPair) -> None:
        self.exchange = self._session.query(Exchange).filter_by(code='binance').first()

        if pair.exchange.id is not self.exchange.id:
            raise Exception('pair does not belongs to {}'.format(self.exchange.name))

        last_timestamp = None
        while True:
            try:
                candles = self.client.get_candles(symbol=pair.symbol, start=last_timestamp)
            except BinanceException:
                # TODO [feature-5] Handle possible exceptions. For example: timeout, throttling, IP Ban
                pass

            if not candles or (last_timestamp is not None and last_timestamp == candles[0]['timestamp']):
                # Reached the end of available candles
                break

            for candle in candles:
                self.add_candlestick(pair, candle)

            last_timestamp = candles[0]['timestamp']

        self._session.commit()

    def populate_currency_pair(self, exchange: Exchange) -> None:
        try:
            symbols = self.client.get_symbols()
        except BinanceException:
            # TODO [feature-5] Handle possible exceptions. For example: timeout, throttling, IP Ban
            pass

        for symbol in symbols:
            currency_base = self.add_currency(symbol['currencyBase'])
            currency_quote = self.add_currency(symbol['currencyQuote'])

            self.add_currency_pair(exchange, symbol['symbol'], currency_base, currency_quote)

    def add_exchange(self) -> Exchange:
        (exchange, _) = sqlalchemy_get_or_create.update_or_create(
            self._session,
            Exchange,
            code='binance',
            defaults={'name': 'Binance Exchange'}
        )

        return exchange

    def add_currency(self, symbol: str) -> None:
        (currency, _) = sqlalchemy_get_or_create.update_or_create(
            self._session,
            Currency,
            symbol=symbol,
            defaults={'name': symbol}
        )

        return currency

    def add_currency_pair(self, exchange: Exchange, symbol: str, currency_base: Currency, currency_quote: Currency) -> CurrencyPair:
        (currency_pair, _) = sqlalchemy_get_or_create.update_or_create(
            self._session,
            CurrencyPair,
            exchange=exchange,
            symbol=symbol,
            defaults={'currency_base': currency_base, 'currency_quote': currency_quote}
        )

        return currency_pair

    def add_candlestick(self, pair: CurrencyPair, candle_data: list) -> None:
        (candlestick, _) = sqlalchemy_get_or_create.update_or_create(
            self._session,
            Candlestick,
            currency_pair=pair,
            timestamp=candle_data['timestamp'],
            defaults={
                'open': candle_data['open'],
                'high': candle_data['high'],
                'low': candle_data['low'],
                'close': candle_data['close'],
                'volume': candle_data['volume'],
            }
        )

        return candlestick

    def _create_db_session(self) -> Session:
        # TODO TIRAR ISSO DAQUI
        engine = create_engine(os.getenv('DATABASE_URL'))
        Session = sessionmaker(bind=engine)

        return Session()
