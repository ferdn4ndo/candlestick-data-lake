import tornado.web

from app import STATIC_PATH
from controllers import HealthController, IndexController

routes = [
    (r"/", IndexController),
    (r"/health", HealthController),
    # These are required to create an alias of the static files at the root path
    (
        r"/(apple-touch-icon\.png)",
        tornado.web.StaticFileHandler,
        dict(path=STATIC_PATH),
    ),
    (
        r"/(android-chrome-*\.png)",
        tornado.web.StaticFileHandler,
        dict(path=STATIC_PATH),
    ),
    (r"/(favicon\.icon)", tornado.web.StaticFileHandler, dict(path=STATIC_PATH)),
    (r"/(site.webmanifest)", tornado.web.StaticFileHandler, dict(path=STATIC_PATH)),
]
