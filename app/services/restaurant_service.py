from .base_service import BaseService
from ..models import Restaurant


class RestaurantService(BaseService):
    model = Restaurant

    @classmethod
    def get_by_staff_user_id(self, staff_user_id):
        return self.model.query.filter_by(staff_user_id=staff_user_id).first()