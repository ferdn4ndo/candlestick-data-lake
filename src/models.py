from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

# class Dummy(Base):
#    __tablename__ = "dummy"
#    id = Column(Integer, primary_key=True, index=True)
#    dummy = Column(String(250),)
