from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from . import db


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class DeletableModel(BaseModel):
    __abstract__ = True

    is_active = Column(Boolean, default=True, nullable=False)
