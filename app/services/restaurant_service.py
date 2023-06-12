from . import db, Table, MenuItem, MenuCategory, Restaurant


class RestaurantService:
    def create_table(user_id, name):
        # Create a new table for the restaurant
        restaurant = Restaurant.query.filter_by(staff_user_id=user_id).first()
        if not restaurant:
            return {"msg": "Restaurant not found"}, 404

        table = Table(restaurant_id=restaurant.id, name=name)
        db.session.add(table)
        db.session.commit()
        return table.to_dict(), 200

    def get_table(table_id):
        # Retrieve table information
        table = Table.query.get(table_id)
        if not table:
            return {"msg": "No Table found for this table id"}, 404

        return table.to_dict(), 200

    def get_tables_by_restaurant_id(restaurant_id):
        # Retrieve table information
        tables = Table.query.filter_by(restaurant_id=restaurant_id).all()
        if not tables or len(tables) == 0:
            return {"msg": "No tables found for this restaurant"}, 404
        return [table.to_dict() for table in tables], 200

    def update_table(table_id, data, user_id):
        # Update table information
        table = Table.query.get(table_id)
        if not table or table.restaurant.staff_user_id != user_id:
            return {"msg": "Table not found or not authorized"}, 404
        table.name = data.get("name", table.name)
        db.session.commit()
        return table.to_dict(), 200

    def delete_table(table_id, user_id):
        # Delete a table
        table = Table.query.get(table_id)
        if not table or table.restaurant.staff_user_id != user_id:
            return {"msg": "Table not found or not authorized"}, 404

        db.session.delete(table)
        db.session.commit()
        return {"msg": "Category deleted"}, 200

    ################################################################################

    def create_menu_category(user_id, name):
        # Create a new menu category for the restaurant
        restaurant = Restaurant.query.filter_by(staff_user_id=user_id).first()
        if not restaurant:
            return {"msg": "Restaurant not found"}, 404

        menu_category = MenuCategory(restaurant_id=restaurant.id, name=name)
        db.session.add(menu_category)
        db.session.commit()
        return menu_category.to_dict(), 200

    def get_menu_category(category_id):
        # Retrieve menu category information
        category = MenuCategory.query.get(category_id)
        if not category:
            return {"msg": "No category found for this category id"}, 404

        return category.to_dict(), 200

    def get_menu_categories_by_restaurant_id(restaurant_id):
        # Retrieve menu category information
        categories = MenuCategory.query.filter_by(restaurant_id=restaurant_id).all()
        if not categories or len(categories) == 0:
            return {"msg": "No categories found for this restaurant"}, 404
        return [category.to_dict() for category in categories], 200

    def update_menu_category(category_id, data, user_id):
        # Update menu information
        menu_category = MenuCategory.query.get(category_id)
        if not menu_category or menu_category.restaurant.staff_user_id != user_id:
            return {"msg": "Category not found or not authorized"}, 404
        menu_category.name = data.get("name", menu_category.name)
        db.session.commit()
        return menu_category.to_dict(), 200

    def delete_menu_category(category_id, user_id):
        # Delete a menu
        menu_category = MenuCategory.query.get(category_id)
        if not menu_category or menu_category.restaurant.staff_user_id != user_id:
            return {"msg": "Category not found or not authorized"}, 404

        db.session.delete(menu_category)
        db.session.commit()
        return {"msg": "Category deleted"}, 200

    ################################################################################

    def create_menu_item(user_id, category_id, name, description, price, image):
        menu_category = MenuCategory.query.get(category_id)
        if not menu_category or menu_category.restaurant.staff_user_id != user_id:
            return {"msg": "Category not found or not authorized"}, 404

        # Create a new menu item for a menu
        menu_item = MenuItem(
            category_id=category_id,
            name=name,
            description=description,
            price=price,
            image=image,
        )
        db.session.add(menu_item)
        db.session.commit()
        return menu_item.to_dict(), 200

    def get_menu_item(item_id):
        # Retrieve menu item information
        item = MenuItem.query.get(item_id)
        if not item:
            return {"msg": "No item found for this item id"}, 404

        return item.to_dict(), 200

    def get_menu_items_by_category_id(category_id):
        # Retrieve menu item information
        items = MenuItem.query.filter_by(category_id=category_id).all()
        if not items or len(items) == 0:
            return {"msg": "No items found for this category"}, 404
        return [item.to_dict() for item in items], 200

    def update_menu_item(item_id, data, user_id):
        # Update menu item information
        menu_item = MenuItem.query.get(item_id)
        if not menu_item or menu_item.category.restaurant.staff_user_id != user_id:
            return {"msg": "Item not found or not authorized"}, 404

        # Ensure category_id is not from another restaurant
        category_id = data.get("category_id", menu_item.category_id)
        new_category = MenuCategory.query.get(category_id)
        if new_category and new_category.restaurant.staff_user_id != user_id():
            return {"msg": "Can't update to an unauthorized category"}, 403

        menu_item.category_id = category_id
        menu_item.name = data.get("name", menu_item.name)
        menu_item.description = data.get("description", menu_item.description)
        menu_item.price = data.get("price", menu_item.price)
        menu_item.image = data.get("image", menu_item.image)
        db.session.commit()
        return menu_item.to_dict(), 200

    def delete_menu_item(item_id, user_id):
        # Delete a menu item
        menu_item = MenuItem.query.get(item_id)
        if not menu_item or menu_item.category.restaurant.staff_user_id != user_id:
            return {"msg": "Item not found or not authorized"}, 404

        db.session.delete(menu_item)
        db.session.commit()
        return {"msg": "Item deleted"}, 200
