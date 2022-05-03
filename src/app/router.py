import tornado.web

from app import STATIC_PATH
from app.controllers import (
    HealthController,
    IndexController,
    ExchangeListController,
    ExchangeSingleController,
    ExchangeStreamListController,
    ExchangeStreamSingleController,
    ExchangeHistoricalListController,
    ExchangeHistoricalSingleController,
    ExchangeSetupController,
)

routes = [
    (r"/", IndexController),
    (r"/health", HealthController),
    (r"/exchanges", ExchangeListController),
    (r"/exchanges/(?P<exchange_id>\w+)", ExchangeSingleController),
    (r"/exchanges/(?P<exchange_id>\w+)/streams", ExchangeStreamListController),
    (r"/exchanges/(?P<exchange_id>\w+)/streams/(?P<pair>\w+)", ExchangeStreamSingleController),
    (r"/exchanges/(?P<exchange_id>\w+)/historical", ExchangeHistoricalListController),
    (r"/exchanges/(?P<exchange_id>\w+)/historical/(?P<pair>\w+)", ExchangeHistoricalSingleController),
    (r"/exchanges/(?P<exchange_id>\w+)/setup", ExchangeSetupController),
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
