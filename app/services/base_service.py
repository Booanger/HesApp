from abc import ABC, abstractmethod
from . import db

class BaseService():
    model = None
    db = db

    @classmethod
    def create(cls, data):
        instance = cls.model(**data)
        cls.db.session.add(instance)
        cls.db.session.commit()
        return instance

    @classmethod
    def get(cls, id):
        return cls.model.query.get(id)

    @classmethod
    def update(cls, id, data):
        instance = cls.model.query.get(id)
        for key, value in data.items():
            setattr(instance, key, value)
        cls.db.session.commit()
        return instance

    @classmethod
    def delete(cls, id):
        instance = cls.model.query.get(id)
        cls.db.session.delete(instance)
        cls.db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.model.query.all()