import tornado.ioloop
import tornado.web

from app import STATIC_PATH, APP_PORT, DEVELOPMENT_MODE
from app.router import routes
from app.services import DatabaseService


def make_app():
    if DEVELOPMENT_MODE:
        print("Starting in DEBUG/DEVELOPMENT mode at port {}".format(APP_PORT))

    return tornado.web.Application(
        routes,
        db=DatabaseService.get_db(),
        debug=DEVELOPMENT_MODE,
        static_path=STATIC_PATH,
    )


if __name__ == "__main__":
    tornado_app = make_app()
    tornado_app.listen(APP_PORT)
    loop = tornado.ioloop.IOLoop.current()
    loop.start()
