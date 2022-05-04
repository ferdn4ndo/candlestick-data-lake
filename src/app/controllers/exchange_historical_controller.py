from datetime import datetime
import json
import logging

from tornado import gen
from tornado.ioloop import IOLoop
from tornado import concurrent

from app.controllers.base_controller import BaseController
from app.errors import ResourceAlreadyInUseError
from app.services.consumer_service import ConsumerService
from app.services.consumer_service_factory import (
    create_consumer_service_from_exchange,
    create_client_from_exchange_code,
    create_service_from_exchange_code,
)
from app.services.currency_pair.currency_pair_service import CurrencyPairService
from app.services.database_service import DatabaseService
from app.services.exchanges.exchange_service_factory import create_exchange_service_from_id, get_exchange_by_id


class ExchangeHistoricalListController(BaseController):
    def get(self) -> None:
        self.write(self.send_error_response(status_code=405, message=f"The setup action requires a POST request!"))

    @gen.coroutine
    def post(self, **kwargs) -> None:
        body = json.loads(self.request.body)
        if "symbol" not in body:
            self.send_error(status_code=400, reason="The 'symbol' field is required.")

        exchange_id = kwargs.get("exchange_id")
        symbol = body["symbol"]

        with DatabaseService.create_session() as session:
            exchange = get_exchange_by_id(session=session, exchange_id=exchange_id)
            exchange_code = exchange.code
            CurrencyPairService.check_if_symbol_exists(session=session, exchange=exchange, symbol=symbol)

        try:
            CurrencyPairService.check_in_use(
                agent=ConsumerService.AGENT_NAME,
                exchange_code=exchange.code,
                pair_symbol=symbol,
            )
        except ResourceAlreadyInUseError as ex:
            self.send_error_response(status_code=409, message=str(ex))
            return

        CurrencyPairService.set_in_use(
            pair_symbol=symbol,
            exchange_code=exchange_code,
            agent=ConsumerService.AGENT_NAME,
            raise_error=True,
            file_content=datetime.now().isoformat(),
        )

        logging.info(f"Calling background fetching of pair symbol '{symbol}' from '{exchange_code}'.")

        exchange_client = create_client_from_exchange_code(exchange_code=exchange_code)
        exchange_service = create_service_from_exchange_code(exchange_code=exchange_code)

        executor = concurrent.futures.ThreadPoolExecutor(8)

        executor.submit(
            ConsumerService.fetch_currency_pair_candles_in_background,
            client=exchange_client,
            service=exchange_service,
            exchange_code=exchange_code,
            pair_symbol=symbol,
        )

        self.set_status(status_code=202, reason="The request was accepted and is being processed in background.")
        self.write({"message": f"Successfully started fetching data from '{exchange_code}' for symbol '{symbol}'."})


class ExchangeHistoricalSingleController(BaseController):
    def get(self) -> None:
        self.write(self.send_error_response(status_code=405, message=f"The setup action requires a DELETE request!"))

    def delete(self, **kwargs) -> None:
        exchange_id = kwargs.get("exchange_id")
        pair = kwargs.get("pair")

        with DatabaseService.create_session() as session:
            exchange = get_exchange_by_id(session=session, exchange_id=exchange_id)
            exchange_code = exchange.code
            CurrencyPairService.check_if_symbol_exists(session=session, exchange=exchange, symbol=pair)

        try:
            CurrencyPairService.check_in_use(
                agent=ConsumerService.AGENT_NAME,
                exchange_code=exchange.code,
                pair_symbol=pair,
            )

            self.send_error_response(
                status_code=409, message=f"The pair symbol '{pair}' is not currently in use by '{exchange_code}'!"
            )
        except ResourceAlreadyInUseError as ex:
            logging.info(f"Changing flag to abort background fetching of pair symbol '{pair}' from '{exchange_code}'.")

            CurrencyPairService.reset_in_use(
                agent=ConsumerService.AGENT_NAME,
                exchange_code=exchange.code,
                pair_symbol=pair,
            )

            self.write(
                {
                    "message": f"Candlestick background fetching for pair symbol '{pair}' from '{exchange_code}' was stopped!"
                }
            )
