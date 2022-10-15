from app.controllers.base_controller import BaseController


class ExchangeStreamListController(BaseController):
    def get(self, **kwargs) -> None:
        exchange_id = kwargs.get("exchange_id")

        self.write(exchange_id)


class ExchangeStreamSingleController(BaseController):
    def get(self, **kwargs) -> None:
        exchange_id = kwargs.get("exchange_id")

        self.write(exchange_id)
