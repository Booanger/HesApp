from ..models import db, User

print("user service.py")

class UserService:
    @staticmethod
    def create_user(data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def update_user(id, data):
        user = User.query.get(id)
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def delete_user(id):
        User.query.filter_by(id=id).delete()
        db.session.commit()

    @staticmethod
    def get_users():
        return User.query.all()
