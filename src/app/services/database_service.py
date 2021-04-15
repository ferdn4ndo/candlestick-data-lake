import os

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from tornado_sqlalchemy import SQLAlchemy


class DatabaseService:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def get_db() -> SQLAlchemy:
        return SQLAlchemy(os.getenv("DATABASE_URL"))

    def get_or_create(self, model, defaults=None, **kwargs):
        try:
            return self.session.query(model).filter_by(**kwargs).one(), False
        except NoResultFound:
            params = self._extract_model_params(defaults, **kwargs)

            return self._create_object_from_params(model, kwargs, params)

    def update_or_create(self, model, defaults:dict = None, **kwargs):
        defaults = defaults or {}

        with self.session.begin_nested():
            try:
                obj = self.session.query(model).with_for_update().filter_by(**kwargs).one()
            except NoResultFound:
                params = self._extract_model_params(defaults, **kwargs)
                obj, created = self._create_object_from_params(model, kwargs, params, lock=True)

                if created:
                    return obj, created

            for k, v in defaults.items():
                setattr(obj, k, v)

            self.session.add(obj)
            self.session.flush()

        return obj, False

    def _create_object_from_params(self, model, lookup: dict, params: dict, lock=False):
        obj = model(**params)

        self.session.add(obj)

        try:
            with self.session.begin_nested():
                self.session.flush()
        except IntegrityError:
            self.session.rollback()

            query = self.session.query(model).filter_by(**lookup)

            if lock:
                query = query.with_for_update()

            try:
                obj = query.one()
            except NoResultFound:
                raise
            else:
                return obj, False
        else:
            return obj, True

    def _extract_model_params(self, defaults: dict, **kwargs) -> dict:
        defaults = defaults or {}

        ret = {}
        ret.update(kwargs)
        ret.update(defaults)

        return ret
