from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from app import DATABASE_URL
from tornado_sqlalchemy import SQLAlchemy

from app.errors import ModelAlreadyExistsError, ResourceNotFoundError


class DatabaseService:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def get_db() -> SQLAlchemy:
        return SQLAlchemy(DATABASE_URL)

    @staticmethod
    def create_session() -> Session:
        engine = create_engine(DATABASE_URL)
        session_maker = sessionmaker(bind=engine)
        return session_maker()

    def get_or_create(self, model, defaults: dict = None, **kwargs):
        try:
            return self.session.query(model).filter_by(**kwargs).one(), False
        except NoResultFound:
            params = self._extract_model_params(defaults, **kwargs)

            return self._create_object_from_params(model, kwargs, params)

    def get_one_by_params(self, model, **kwargs):
        try:
            return self.session.query(model).filter_by(**kwargs).one()
        except NoResultFound:
            raise ResourceNotFoundError

    def update_or_create(self, model, defaults: dict = None, **kwargs):
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

    def create(self, model, defaults: dict = None, **kwargs):
        defaults = defaults or {}
        params = self._extract_model_params(defaults, **kwargs)
        obj = model(**params)

        try:
            self.session.add(obj)
            self.session.commit()
        except IntegrityError as exception:
            if "Duplicate entry" in str(exception):
                raise ModelAlreadyExistsError
            else:
                raise exception

        return obj

    def find_or_create(self, model, defaults: dict = None, **kwargs):
        defaults = defaults or {}

        obj = self.session.query(model).filter_by(**kwargs).first()
        if obj is None:
            obj = self.create(model, defaults=defaults, **kwargs)

        return obj

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
