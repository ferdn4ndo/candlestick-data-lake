import logging
import os

from tornado import concurrent


def is_truly(value) -> bool:
    return str(value).lower() in [
        "true",
        "1",
        "y",
        "yes",
    ]


__version__ = "0.0.1"
APP_PORT = os.getenv("APP_PORT", "8888")
DEVELOPMENT_MODE = is_truly(os.getenv("DEVELOPMENT_MODE", "0"))
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
LOG_LEVEL = os.getenv("LOG_LEVEL", logging.INFO)
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s %(levelname)s %(message)s")
DATE_FORMAT = os.getenv("DATE_FORMAT", "%Y-%m-%d %H:%M:%S")
TEMP_FOLDER_PATH = os.getenv("TEMP_FOLDER_PATH", "/usr/src/app/temp")
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqldb://csdl:csdl@db:3306/csdl")
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME", "csdl")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD", "root")

tornado_app = None

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt=DATE_FORMAT)

executor = concurrent.futures.ThreadPoolExecutor(8)
