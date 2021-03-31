import os


__version__ = "1.0.0"
APP_PORT = os.environ["APP_PORT"] if "APP_PORT" in os.environ else 8888
DEVELOPMENT_MODE = (
    os.environ["DEVELOPMENT_MODE"] == "1" if "DEVELOPMENT_MODE" in os.environ else False
)
tornado_app = None
