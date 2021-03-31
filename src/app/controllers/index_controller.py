from app import __version__

from app.controllers.base_controller import BaseController


class IndexController(BaseController):
    def get(self):
        self.write("CandleStick Data Lake v{}".format(__version__))
