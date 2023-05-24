from ..models import db, MenuCategory, MenuItem

print("menu service.py")

class MenuService:
    @staticmethod
    def create_category(data):
        category = MenuCategory(**data)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def get_categories():
        return MenuCategory.query.all()
    
    @staticmethod
    def update_category(category_id, updated_data):
        category = MenuCategory.query.get(category_id)
        if category:
            for key, value in updated_data.items():
                setattr(category, key, value)
            db.session.commit()
        return category

    @staticmethod
    def delete_category(category_id):
        category = MenuCategory.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            
    ################################################################

    @staticmethod
    def create_item(data):
        item = MenuItem(**data)
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def get_items(category_id):
        return MenuItem.query.filter_by(category_id=category_id).all()

    @staticmethod
    def update_item(item_id, updated_data):
        item = MenuItem.query.get(item_id)
        if item:
            for key, value in updated_data.items():
                setattr(item, key, value)
            db.session.commit()
        return item

    @staticmethod
    def delete_item(item_id):
        item = MenuItem.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
