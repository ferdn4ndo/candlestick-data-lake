from typing import Optional, Awaitable, Any

import tornado.web
from tornado import httputil
from tornado.escape import json_decode


class BaseController(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def prepare(self):
        # Access self.args directly instead of using self.get_argument if input is JSON.
        if "Content-Type" in self.request.headers and self.request.headers["Content-Type"] == "application/x-json":
            self.args = json_decode(self.request.body)
