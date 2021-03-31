import tornado.web

from app import STATIC_PATH
from controllers import HealthController, IndexController

routes = [
    (r"/", IndexController),
    (r"/health", HealthController),
]

# Used to create aliases of some static files required to be exposed at the root path
static_root_routes = [
    (
        r"/(android-chrome-*\.png)",
        tornado.web.StaticFileHandler,
        dict(path=STATIC_PATH),
    ),
    (
        r"/(apple-touch-icon\.png)",
        tornado.web.StaticFileHandler,
        dict(path=STATIC_PATH),
    ),
    (r"/(favicon\.icon)", tornado.web.StaticFileHandler, dict(path=STATIC_PATH)),
    (r"/(site\.webmanifest)", tornado.web.StaticFileHandler, dict(path=STATIC_PATH)),
]
routes.extend(static_root_routes)
