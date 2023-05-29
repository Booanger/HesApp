from cerberus import Validator


register_customer_validator = Validator({
    'first_name': {'type': 'string', 'required': True},
    'last_name': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True, 'minlength': 6},
    'phone': {'type': 'string', 'minlength': 1, 'required': True},
})

register_staff_validator = Validator({
    'first_name': {'type': 'string', 'required': True},
    'last_name': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True, 'minlength': 6},
    'phone': {'type': 'string', 'minlength': 1, 'required': True},
    'restaurant_name': {'type': 'string', 'required': True},
    'restaurant_description': {'type': 'string', 'required': True},
    'restaurant_address': {'type': 'string', 'required': True},
    'restaurant_phone': {'type': 'string', 'required': True},
    'restaurant_logo': {'type': 'string', 'required': False},
})

login_validator = Validator({
    'email': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 120},
    'password': {'type': 'string', 'required': True, 'empty': False, 'minlength': 6},
})

update_user_validator = Validator({
    'first_name': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 50,
        'required': False
    },
    'last_name': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 50,
        'required': False
    },
    'phone': {
        'type': 'string',
        'minlength': 10,
        'maxlength': 20,
        'required': False
    },
    'password': {
        'type': 'string',
        'minlength': 8,
        'required': False
    }
})

restaurant_update_validator = Validator({
    'name': {'type': 'string', 'required': False},
    'description': {'type': 'string', 'required': False},
    'address': {'type': 'string', 'required': False},
    'phone': {'type': 'string', 'required': False},
    'logo': {'type': 'string', 'required': False},
})

create_menu_category_validator = Validator({
    # 'restaurant_id': {'type': 'integer', 'required': True},
    'name': {'type': 'string', 'required': True, 'minlength': 1},
})

create_menu_item_validator = Validator({
    'category_id': {'type': 'integer', 'required': True},
    'name': {'type': 'string', 'required': True, 'minlength': 1},
    'description': {'type': 'string', 'required': False, 'minlength': 1},
    'price': {'type': 'float', 'required': True},
    'image': {'type': 'string', 'required': False},
})

update_menu_category_validator = Validator({
    # 'restaurant_id': {'type': 'integer', 'required': True},
    'name': {'type': 'string', 'required': True, 'minlength': 1},
})

update_menu_item_validator = Validator({
    'category_id': {'type': 'integer', 'required': False},
    'name': {'type': 'string', 'required': False, 'minlength': 1},
    'description': {'type': 'string', 'required': False, 'minlength': 1},
    'price': {'type': 'float', 'required': False},
    'image': {'type': 'string', 'required': False},
})
# TODO add more validators here for other routes or data structures


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

        self.login_model = api.model('Login', {
            'email': fields.String(required=True, description='User email', max_length=120),
            'password': fields.String(required=True, description='User password', min_length=6)
        })

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
