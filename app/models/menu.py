from . import db
from .restaurant import Restaurant

print("menu.py")


class MenuCategory(db.Model):
    __tablename__ = 'menu_categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    name = db.Column(db.String(100))
    
    menu_items = db.relationship('MenuItem', backref='category', lazy='dynamic')


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_categories.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image = db.Column(db.String(200))
    #category = db.relationship('MenuCategory')
    order_items = db.relationship('OrderItem', backref='menu_item', lazy='dynamic')
