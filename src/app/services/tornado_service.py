import tornado.ioloop
import tornado.web

from app import DEVELOPMENT_MODE, APP_PORT, DatabaseService, STATIC_PATH
from app.router import routes
from app.services.temp_file_service import clear_temp_folder


def make_tornado_app():
    mode = "DEBUG/DEVELOPMENT" if DEVELOPMENT_MODE else "PRODUCTION"
    print(f"Starting in {mode} mode at port {APP_PORT}")

    clear_temp_folder()

    return tornado.web.Application(
        routes,
        db=DatabaseService.get_db(),
        debug=DEVELOPMENT_MODE,
        static_path=STATIC_PATH,
    )


def enter_tornado_infinite_loop():
    tornado_app = make_tornado_app()
    tornado_app.listen(APP_PORT)
    loop = tornado.ioloop.IOLoop.current()
    loop.start()
