from typing import Awaitable, Optional

from tornado.escape import json_decode
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin


class BaseController(RequestHandler, SessionMixin):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def prepare(self) -> None:
        # Access self.args directly instead of using self.get_argument if input is JSON.
        if "Content-Type" in self.request.headers and self.request.headers["Content-Type"] == "application/x-json":
            self.args = json_decode(self.request.body)

    def send_error_response(
            self,
            status_code: int = 500,
            message: str = "An unexpected error occurred.",
            extra_payload: dict = None
    ) -> None:
        payload = extra_payload or {}
        payload['message'] = message

        self.set_status(status_code=status_code, reason=message)
        self.write(payload)
