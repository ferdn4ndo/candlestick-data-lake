import json

from app.controllers.base_controller import BaseController
from app.errors.model_already_exists_error import ModelAlreadyExistsError
from app.errors.resource_not_found_error import ResourceNotFoundError
from app.models import Exchange
from app.services.auth_service import auth_required
from app.services.database_service import DatabaseService
from app.services.exchanges.exchange_service_factory import (
    ALLOWED_EXCHANGE_CODES,
    create_exchange_service_from_code,
    serialize_existing_exchanges,
    create_exchange_service_from_model,
)


class ExchangeListController(BaseController):
    def get(self) -> None:
        exchanges = serialize_existing_exchanges()

        self.write({"items": exchanges})

    def post(self) -> None:
        body = json.loads(self.request.body)
        if "code" not in body:
            self.send_error(status_code=400, reason="The 'code' field is required.")

        code = body["code"]
        if code not in ALLOWED_EXCHANGE_CODES:
            self.send_error_response(
                status_code=400,
                message=f"The code '{code}' is invalid. Possible values: {', '.join(ALLOWED_EXCHANGE_CODES)}.",
            )

        try:
            service = create_exchange_service_from_code(code=code)
            service.add_exchange()
            self.write(service.exchange.serialize())
        except ModelAlreadyExistsError:
            self.send_error_response(status_code=409, message=f"The code '{code}' is already registered.")


@auth_required
class ExchangeSingleController(BaseController):
    def get(self, **kwargs) -> None:
        exchange_id = kwargs.get("exchange_id")

        try:
            with DatabaseService.create_session() as session:
                database_service = DatabaseService(session=session)
                exchange = database_service.get_one_by_params(model=Exchange, id=exchange_id)
                exchange_service = create_exchange_service_from_model(exchange=exchange)
                self.write(exchange_service.serialize_exchange())
        except ResourceNotFoundError:
            self.send_error_response(status_code=404, message=f"The exchange ID '{exchange_id}' was not found.")
