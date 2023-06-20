from . import db, Table, MenuItem, MenuCategory, Restaurant


class RestaurantService:
    @staticmethod
    def create_table(user_id, name):
        restaurant = Restaurant.query.filter_by(staff_user_id=user_id).first()
        if not restaurant:
            return {"msg": "Restaurant not found"}, 404

        table = Table(restaurant_id=restaurant.id, name=name)
        db.session.add(table)
        db.session.commit()
        return table.to_dict(), 201  # Use 201 for Created

    @staticmethod
    def get_table(table_id):
        table = Table.query.filter_by(id=table_id, is_active=True).first()
        if not table:
            return {"msg": "No Table found for this table id"}, 404

        return table.to_dict(), 200

    def get_tables_by_restaurant_id(restaurant_id):
        tables = Table.query.filter_by(
            restaurant_id=restaurant_id, is_active=True
        ).all()
        return [table.to_dict() for table in tables], 200

    @staticmethod
    def update_table(table_id, data, user_id):
        table = Table.query.filter_by(id=table_id, is_active=True).first()
        if not table:
            return {"msg": "Table not found"}, 404
        if table.restaurant.staff_user_id != user_id:
            return {"msg": "Access denied"}, 403
        table.name = data.get("name", table.name)
        db.session.commit()
        return table.to_dict(), 200

    @staticmethod
    def delete_table(table_id, user_id):
        table = Table.query.filter_by(id=table_id, is_active=True).first()
        if not table:
            return {"msg": "Table not found"}, 404
        if table.restaurant.staff_user_id != user_id:
            return {"msg": "Access denied"}, 403

        table.is_active = False
        db.session.commit()
        return {"msg": "Category deleted"}, 204  # Use 204 for No Content

    ################################################################################

    @staticmethod
    def create_menu_category(user_id, name):
        restaurant = Restaurant.query.filter_by(staff_user_id=user_id).first()
        if not restaurant:
            return {"msg": "Restaurant not found"}, 404

        menu_category = MenuCategory(restaurant_id=restaurant.id, name=name)
        db.session.add(menu_category)
        db.session.commit()
        return menu_category.to_dict(), 201

    @staticmethod
    def get_menu_category(category_id):
        category = MenuCategory.query.filter_by(id=category_id, is_active=True).first()
        if not category:
            return {"msg": "No category found for this category id"}, 404

        return category.to_dict(), 200

    @staticmethod
    def get_menu_categories_by_restaurant_id(restaurant_id):
        categories = MenuCategory.query.filter_by(
            restaurant_id=restaurant_id, is_active=True
        ).all()
        return [category.to_dict() for category in categories], 200

    @staticmethod
    def update_menu_category(category_id, data, user_id):
        menu_category = MenuCategory.query.filter_by(
            id=category_id, is_active=True
        ).first()
        if not menu_category:
            return {"msg": "Category not found"}, 404
        if menu_category.restaurant.staff_user_id != user_id:
            return {"msg": "Access denied"}, 403
        menu_category.name = data.get("name", menu_category.name)
        db.session.commit()
        return menu_category.to_dict(), 200

    @staticmethod
    def delete_menu_category(category_id, user_id):
        menu_category = MenuCategory.query.filter_by(
            id=category_id, is_active=True
        ).first()
        if not menu_category:
            return {"msg": "Category not found"}, 404
        if menu_category.restaurant.staff_user_id != user_id:
            return {"msg": "Access denied"}, 403

        menu_category.is_active = False
        db.session.commit()
        return {"msg": "Category deleted"}, 204

    ################################################################################

    @staticmethod
    def create_menu_item(user_id, category_id, name, description, price, image):
        menu_category = MenuCategory.query.get(category_id)
        if not menu_category:
            return {"msg": "Category not found"}, 404
        if menu_category.restaurant.staff_user_id != user_id:
            return {"msg": "Access denied"}, 403

        menu_item = MenuItem(
            category_id=category_id,
            name=name,
            description=description,
            price=price,
            image=image,
        )
        db.session.add(menu_item)
        db.session.commit()
        return menu_item.to_dict(), 201

    @staticmethod
    def get_menu_item(item_id):
        item = MenuItem.query.filter_by(id=item_id, is_active=True)
        if not item:
            return {"msg": "No item found for this item id"}, 404

        return item.to_dict(), 200

    @staticmethod
    def get_menu_items_by_category_id(category_id):
        items = MenuItem.query.filter_by(category_id=category_id, is_active=True).all()
        return [item.to_dict() for item in items], 200

    @staticmethod
    def update_menu_item(item_id, data, user_id):
        menu_item = MenuItem.query.filter_by(id=item_id, is_active=True).first()
        if not menu_item:
            return {"msg": "Item not found"}, 404
        if menu_item.category.restaurant.staff_user_id != user_id:
            return {"msg": "Access denied"}, 403

        category_id = data.get("category_id", menu_item.category_id)
        new_category = MenuCategory.query.get(category_id)
        if new_category and new_category.restaurant.staff_user_id != user_id:
            return {"msg": "Access denied"}, 403

        menu_item.category_id = category_id
        menu_item.name = data.get("name", menu_item.name)
        menu_item.description = data.get("description", menu_item.description)
        menu_item.price = data.get("price", menu_item.price)
        menu_item.image = data.get("image", menu_item.image)
        db.session.commit()
        return menu_item.to_dict(), 200

    @staticmethod
    def delete_menu_item(item_id, user_id):
        menu_item = MenuItem.query.filter_by(id=item_id, is_active=True).first()
        if not menu_item:
            return {"msg": "Item not found"}, 404
        if menu_item.category.restaurant.staff_user_id != user_id:
            return {"msg": "Not authorized"}, 403

        # menu_item.category_id = None

        menu_item.is_active = False
        db.session.commit()
        return {"msg": "Item deleted"}, 204
