from .base_service import BaseService
from ..models import MenuCategory, MenuItem


class MenuCategoryService(BaseService):
    model = MenuCategory

    @classmethod
    def get_all_by_restaurant_id(self, restaurant_id):
        return self.model.query.filter_by(restaurant_id=restaurant_id).all()


class MenuItemService(BaseService):
    model = MenuItem

    @classmethod
    def get_all_by_category_id(self, category_id):
        return self.model.query.filter_by(category_id=category_id).all()
