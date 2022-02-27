import json
import logging

from tornado import gen
from tornado.ioloop import IOLoop

from app.controllers.base_controller import BaseController
from app.errors import ResourceAlreadyInUseError
from app.services.consumer_service import ConsumerService
from app.services.consumer_service_factory import create_consumer_service_from_exchange, \
    create_client_from_exchange_code, create_service_from_exchange_code
from app.services.currency_pair.currency_pair_service import CurrencyPairService
from app.services.database_service import DatabaseService
from app.services.exchanges.exchange_service_factory import create_exchange_service_from_id, get_exchange_by_id


class ExchangeHistoricalListController(BaseController):
    def get(self, **kwargs) -> None:
        exchange_id = kwargs.get('exchange_id')

        with DatabaseService.create_session() as session:
            service = create_exchange_service_from_id(session=session, exchange_id=exchange_id)
            currency_pairs = service.list_currency_pairs()


        self.write(exchange_id)

    @gen.coroutine
    def post(self, **kwargs) -> None:
        body = json.loads(self.request.body)
        if 'symbol' not in body:
            self.send_error(status_code=400, reason="The 'symbol' field is required.")

        exchange_id = kwargs.get('exchange_id')
        symbol = body['symbol']

        with DatabaseService.create_session() as session:
            exchange = get_exchange_by_id(session=session, exchange_id=exchange_id)
            exchange_code = exchange.code
            CurrencyPairService.check_if_symbol_exists(session=session, exchange=exchange, symbol=symbol)

        in_use = CurrencyPairService.is_in_use(
            agent=ConsumerService.AGENT_NAME,
            pair_symbol=symbol,
            exchange_code=exchange.code
        )

        if in_use:
            raise ResourceAlreadyInUseError(
                f"The pair symbol '{symbol}' is already being fetched from '{exchange_code}'."
            )

        logging.info(
            f"Calling background fetching of pair symbol '{symbol}' from '{exchange_code}'."
        )

        exchange_client = create_client_from_exchange_code(exchange_code=exchange_code)
        exchange_service = create_service_from_exchange_code(exchange_code=exchange_code)

        ###
        ### FERNANDO: não dá erro e a tarefa é executada, mas bloqueia qualquer outra chamada via API até ela acabar
        ###

        IOLoop.current().spawn_callback(
            ConsumerService.fetch_currency_pair_candles_in_background,
            client=exchange_client,
            service=exchange_service,
            exchange_code=exchange_code,
            pair_symbol=symbol,
        )

        self.set_status(status_code=202, reason="The request was accepted and is being processed in background.")
        self.write(
            {'message': f"Successfully started fetching data from '{exchange_code}' for symbol '{symbol}'."}
        )


class ExchangeHistoricalSingleController(BaseController):
    def get(self, **kwargs) -> None:
        exchange_id = kwargs.get('exchange_id')

        self.write(exchange_id)
