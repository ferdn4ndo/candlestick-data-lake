import logging
import os
from abc import ABC

from datetime import datetime
from sqlalchemy import DECIMAL, BigInteger, Column, DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import backref, relationship
from tornado_sqlalchemy import SQLAlchemy

db = SQLAlchemy(url=os.getenv("DATABASE_URL"))
from sqlalchemy.orm import relationship

from app.services import DatabaseService

db = DatabaseService.get_db()


class BaseModel(db.Model):
    __abstract__ = True

    def serialize(self):
        return {column.name: str(getattr(self, column.name)) for column in self.__table__.columns}

    def unserialize(self, data):
        for column, value in data.items():
            if hasattr(self, column):
                setattr(self, column, value)
            else:
                logging.warning(f"Filed {column} was not recognized during unserialize (value: {value})")


class Exchange(BaseModel):
    __tablename__ = "exchange"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), nullable=False, unique=True)
    name = Column(String(20), nullable=False)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class Currency(BaseModel):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False, unique=True)
    name = Column(String(20))

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class CurrencyPair(BaseModel):
    __tablename__ = "currency_pair"
    __table_args__ = (UniqueConstraint("exchange_id", "symbol"),)

    id = Column(Integer, primary_key=True, index=True)
    exchange_id = Column(Integer, ForeignKey("exchange.id"))
    currency_base_id = Column(Integer, ForeignKey("currency.id"))
    currency_quote_id = Column(Integer, ForeignKey("currency.id"))
    symbol = Column(String(20), nullable=False, unique=True)

    exchange = relationship("Exchange")
    currency_base = relationship("Currency", foreign_keys=[currency_base_id])
    currency_quote = relationship("Currency", foreign_keys=[currency_quote_id])

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class Candlestick(BaseModel):
    __tablename__ = "candlestick"
    __table_args__ = (UniqueConstraint("currency_pair_id", "timestamp"),)

    id = Column(Integer, primary_key=True, index=True)
    currency_pair_id = Column(Integer, ForeignKey("currency_pair.id"))
    timestamp = Column(BigInteger, nullable=False)
    open = Column(DECIMAL(precision=16, scale=8), nullable=False)
    high = Column(DECIMAL(precision=16, scale=8), nullable=False)
    low = Column(DECIMAL(precision=16, scale=8), nullable=False)
    close = Column(DECIMAL(precision=16, scale=8), nullable=False)
    volume = Column(DECIMAL(precision=16, scale=8), nullable=False)

    currency_pair = relationship("CurrencyPair")

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
