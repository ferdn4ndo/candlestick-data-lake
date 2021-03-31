import os

from tornado_sqlalchemy import SQLAlchemy


class DatabaseService:
    @staticmethod
    def get_db():
        return SQLAlchemy(os.getenv("DATABASE_URL"))
