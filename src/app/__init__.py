import os


__version__ = "0.0.1"
APP_PORT = os.environ["APP_PORT"] if "APP_PORT" in os.environ else 8888
DEVELOPMENT_MODE = (
    os.environ["DEVELOPMENT_MODE"] == "1" if "DEVELOPMENT_MODE" in os.environ else False
)
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
tornado_app = None
