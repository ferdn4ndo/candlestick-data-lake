import logging
from app.clients.client_base import ClientBase
from app.clients.client_exception import ClientException
from app.models import CurrencyPair
from app.services.exchanges.exchange_service_base import ExchangeServiceBase
from sqlalchemy.orm.exc import NoResultFound


class ConsumerService:
    def __init__(self, client: ClientBase, service: ExchangeServiceBase) -> None:
        self.client = client
        self.service = service

    def populate_exchange_data(self) -> None:
        exchange = self.service.add_exchange()

        try:
            symbols = self.client.get_symbols()
        except ClientException:
            # TODO [feature-5] Handle possible exceptions. For example: timeout, throttling, IP Ban
            pass

        for symbol in symbols:
            currency_base = self.service.add_currency(symbol["currencyBase"])
            currency_quote = self.service.add_currency(symbol["currencyQuote"])

            self.service.add_currency_pair(exchange, symbol["symbol"], currency_base, currency_quote)

            self.service.database.session.commit()

    def populate_candlesticks(self, pair_symbol: str) -> None:
        logging.info("Starting populate for {}".format(pair_symbol))

        exchange = self.service.add_exchange()
        try:
            pair = (
                self.service.database.session.query(CurrencyPair).filter_by(symbol=pair_symbol, exchange=exchange).one()
            )
        except NoResultFound:
            raise Exception("Pair {} does not belong to {}".format(pair_symbol, self.service.EXCHANGE_CODE))

        last_timestamp = None
        while True:
            logging.info("Getting candles from {}".format(last_timestamp))
            
            try:
                candles = self.client.get_candles(symbol=pair.symbol, end=last_timestamp)
            except ClientException:
                # TODO [feature-5] Handle possible exceptions. For example: timeout, throttling, IP Ban
                raise Exception("Unable to execute the get_candles method for the timestamp {}".format(last_timestamp))

            if not candles or (last_timestamp is not None and last_timestamp == candles[0]["timestamp"]):
                # Reached the end of available candles
                break

            for candle in candles:
                self.service.add_candlestick(pair, candle)

            self.service.database.session.commit()

            last_timestamp = candles[0]["timestamp"]
