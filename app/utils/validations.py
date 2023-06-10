from flask_restx import fields

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class RestxValidation(metaclass=Singleton):
    def __init__(self, api):
        self.api = api

        self.login_model = api.model(
            'Login', {
            'email': fields.String(required=True, description='User email', max_length=120),
            'password': fields.String(required=True, description='User password', min_length=6)
            },
            strict=True
        )

        self.register_customer_model = api.model('RegisterCustomer', {
            'first_name': fields.String(required=True, description='First name'),
            'last_name': fields.String(required=True, description='Last name'),
            'email': fields.String(required=True, description='Email address'),
            'password': fields.String(required=True, description='Password', min_length=6),
            'phone': fields.String(required=True, description='Phone number', min_length=1)
        })

        self.register_staff_model = api.model('RegisterStaff', {
            'first_name': fields.String(required=True, description='First name'),
            'last_name': fields.String(required=True, description='Last name'),
            'email': fields.String(required=True, description='Email address'),
            'password': fields.String(required=True, description='Password', min_length=6),
            'phone': fields.String(required=True, description='Phone number', min_length=1),
            'restaurant_name': fields.String(required=True, description='Restaurant name'),
            'restaurant_description': fields.String(required=True, description='Restaurant description'),
            'restaurant_address': fields.String(required=True, description='Restaurant address'),
            'restaurant_phone': fields.String(required=True, description='Restaurant phone'),
            'restaurant_logo': fields.String(required=False, description='Restaurant logo'),
        })

        self.update_user_model = api.model('UpdateUser', {
            'first_name': fields.String(required=False, description='First name', min_length=1, max_length=50),
            'last_name': fields.String(required=False, description='Last name', min_length=1, max_length=50),
            'phone': fields.String(required=False, description='Phone number', min_length=10, max_length=20),
            'password': fields.String(required=False, description='Password', min_length=8),
        })

        self.restaurant_update_model = api.model('UpdateRestaurant', {
            'name': fields.String(required=False, description='Restaurant name'),
            'description': fields.String(required=False, description='Restaurant description'),
            'address': fields.String(required=False, description='Restaurant address'),
            'phone': fields.String(required=False, description='Restaurant phone'),
            'logo': fields.String(required=False, description='Restaurant logo'),
        })

        self.create_menu_category_model = api.model('CreateMenuCategory', {
            'name': fields.String(required=True, description='Category name', min_length=1),
        })

        self.create_menu_item_model = api.model('CreateMenuItem', {
            'category_id': fields.Integer(required=True, description='Category ID'),
            'name': fields.String(required=True, description='Menu item name', min_length=1),
            'description': fields.String(required=False, description='Menu item description', min_length=1),
            'price': fields.Float(required=True, description='Menu item price'),
            'image': fields.String(required=False, description='Menu item image'),
        })

        self.update_menu_category_model = api.model('UpdateMenuCategory', {
            'name': fields.String(required=True, description='Category name', min_length=1),
        })

        self.update_menu_item_model = api.model('UpdateMenuItem', {
            'category_id': fields.Integer(required=False, description='Category ID'),
            'name': fields.String(required=False, description='Menu item name', min_length=1),
            'description': fields.String(required=False, description='Menu item description', min_length=1),
            'price': fields.Float(required=False, description='Menu item price'),
            'image': fields.String(required=False, description='Menu item image'),
        })

        self.create_table_model = api.model('CreateTable', {
            'name': fields.String(required=True, description='Table name'),
            'description': fields.String(required=False, description='Table description'),
            'capacity': fields.Integer(required=True, description='Table capacity')
        })
        
        self.update_table_model = api.model('UpdateTable', {
            'name': fields.String(required=False, description='Table name'),
            'description': fields.String(required=False, description='Table description'),
            'capacity': fields.Integer(required=False, description='Table capacity')
        })