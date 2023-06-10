from .base_service import BaseService
from ..models import User


class UserService(BaseService):
    model = User

    @classmethod
    def get_by_email(cls, email):
        return cls.model.query.filter_by(email=email).first()