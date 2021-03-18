import datetime
from sqlalchemy import Column, Enum, Integer, String, DateTime, ForeignKey, BigInteger, DECIMAL
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from markets import Markets

Base = declarative_base()

# class Dummy(Base):
#    __tablename__ = "dummy"
#    id = Column(Integer, primary_key=True, index=True)
#    dummy = Column(String(250),)


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(4), nullable=False, unique=True)
    name = Column(String(20), nullable=False)
    precision = Column(Integer)

    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    upated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Exchange(Base):
    __tablename__ = "exchange"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), nullable=False, unique=True)
    name = Column(String(20), nullable=False)

    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    upated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class CurrencyPair(Base):
    __tablename__ = "currency_pair"

    id = Column(Integer, primary_key=True, index=True)
    exchange_id = Column(Integer, ForeignKey('exchange.id'))
    currency_a_id = Column(Integer, ForeignKey('currency.id'))
    currency_b_id = Column(Integer, ForeignKey('currency.id'))
    symbol = Column(String(10), nullable=False, unique=True)
    market = Column(String(10), Enum(Markets))

    exchange = relationship("Exchange")
    currency_a = relationship("Currency", foreign_keys=[currency_a_id])
    currency_b = relationship("Currency", foreign_keys=[currency_b_id])

    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    upated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Candlestick(Base):
    __tablename__ = "candlestick"

    id = Column(Integer, primary_key=True, index=True)
    open = Column(DECIMAL(precision=16, scale=8), nullable=False)
    high = Column(DECIMAL(precision=16, scale=8), nullable=False)
    low = Column(DECIMAL(precision=16, scale=8), nullable=False)
    close = Column(DECIMAL(precision=16, scale=8), nullable=False)
    volume = Column(DECIMAL(precision=16, scale=8), nullable=False)
    timestamp = Column(BigInteger, nullable=False)
    currency_pair_id = Column(Integer, ForeignKey('currency_pair.id'))

    currency_pair = relationship("CurrencyPair")

    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    upated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
