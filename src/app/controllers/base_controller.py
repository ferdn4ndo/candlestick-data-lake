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
