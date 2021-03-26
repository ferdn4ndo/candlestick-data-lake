import os

import tornado.ioloop
import tornado.web

from tornado_sqlalchemy import SQLAlchemy


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
        ],
        db=SQLAlchemy(os.getenv('DATABASE_URL'))
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
