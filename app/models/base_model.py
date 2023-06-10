from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from . import db

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)