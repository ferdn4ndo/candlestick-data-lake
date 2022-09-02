import logging

from app.clients.client_exception import ClientException
from app.controllers.base_controller import BaseController
from app.services.database_service import DatabaseService
from app.services.exchanges.exchange_service_factory import get_exchange_by_id
from app.services.setup_service import SetupService


class ExchangeSetupController(BaseController):
    def get(self) -> None:
        self.write(self.send_error_response(status_code=405, message=f"The setup action requires a POST request!"))

    def post(self, **kwargs) -> None:
        exchange_id = kwargs.get("exchange_id")

        try:
            with DatabaseService.create_session() as session:
                exchange = get_exchange_by_id(session=session, exchange_id=exchange_id)
                exchange_code = exchange.code

                SetupService.setUpExchange(session=session, exchange_code=exchange_code)

            self.write({"message": f"Setup finished successfully for exchange '{exchange_code}'!"})
        except ClientException as ex:
            logging.error(f"Exchange exception: {ex}")
            self.send_error_response(
                status_code=500, message=f"Error while executing client for exchange '{exchange_code}'!"
            )
