import os


__version__ = "0.0.1"
APP_PORT = os.getenv("APP_PORT", "8888")
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "0").lower() in [
    "true",
    "1",
    "y",
    "yes",
]
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
tornado_app = None
