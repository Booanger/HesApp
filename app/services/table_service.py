from .base_service import BaseService
from ..models import Table


class TableService(BaseService):
    model = Table

    @classmethod
    def get_all_by_restaurant_id(self, restaurant_id):
        return self.model.query.filter_by(restaurant_id=restaurant_id).first()
