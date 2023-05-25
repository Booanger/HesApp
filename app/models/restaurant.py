from . import db
from .user import User

print("restaurant.py")

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    logo = db.Column(db.String(200))
    
    menu_categories = db.relationship('MenuCategory', backref='restaurant', lazy='dynamic')
    orders = db.relationship('Order', backref='restaurant', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'staff_user_id': self.staff_user_id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'phone': self.phone,
            'logo': self.logo,
        }
