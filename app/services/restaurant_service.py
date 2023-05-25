from ..models import db, Restaurant

print("restaurant service.py")

class RestaurantService:
    @staticmethod
    def create_restaurant(data):
        restaurant = Restaurant(**data)
        db.session.add(restaurant)
        db.session.commit()
        return restaurant

    @staticmethod
    def get_restaurant(id):
        return Restaurant.query.get(id)

    @staticmethod
    def get_restaurant_by_staff_user_id(staff_user_id):
        return Restaurant.query.filter_by(staff_user_id=staff_user_id).first()

    @staticmethod
    def update_restaurant(id, data):
        restaurant = Restaurant.query.get(id)
        for key, value in data.items():
            setattr(restaurant, key, value)
        db.session.commit()
        return restaurant

    @staticmethod
    def delete_restaurant(id):
        Restaurant.query.filter_by(id=id).delete()
        db.session.commit()

    @staticmethod
    def get_restaurants():
        return Restaurant.query.all()
