from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .. import enums
from .menu import MenuCategory, MenuItem
from .order import Order, OrderItem
from .payment import PaymentTransaction
from .restaurant import Restaurant
from .user import User
from .table import Table
