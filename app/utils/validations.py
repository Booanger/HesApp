from flask_restx import fields  # , ValidationError

# from flask_restx.inputs import email
# from flask_restx.reqparse import RequestParser
# import re
# import phonenumbers
# from phonenumbers import phonenumberutil


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
            "Login",
            {
                "email": fields.String(
                    required=True,
                    description="User email",
                    max_length=120,
                    pattern=r"^[\w\.\-]+@([\w\-]+\.)+[\w\-]{2,4}$",
                    example="example@example.com",
                    error_message={
                        "pattern": "Invalid email format. Please provide a valid email address."
                    },
                ),
                "password": fields.String(
                    required=True,
                    description="User password",
                    min_length=6,
                    max_length=25,
                ),
            },
            strict=True,
        )

        self.register_customer_model = api.model(
            "RegisterCustomer",
            {
                "username": fields.String(
                    required=True, description="Username", min_length=3, max_length=100
                ),
                "email": fields.String(
                    required=True,
                    description="Email address",
                    max_length=120,
                    pattern=r"^[\w\.\-]+@([\w\-]+\.)+[\w\-]{2,4}$",
                    example="example@example.com",
                    error_messages={
                        "pattern": "Invalid email format. Please provide a valid email address."
                    },
                ),
                "password": fields.String(
                    required=True, description="Password", min_length=6, max_length=25
                ),
                "phone": fields.String(
                    required=True,
                    description="Phone number",
                    min_length=1,
                    max_length=20,
                ),
            },
        )

        self.register_staff_model = api.model(
            "RegisterStaff",
            {
                "username": fields.String(
                    required=True, description="Username", min_length=3, max_length=100
                ),
                "email": fields.String(
                    required=True,
                    description="Email address",
                    max_length=120,
                    pattern=r"^[\w\.\-]+@([\w\-]+\.)+[\w\-]{2,4}$",
                    example="example@example.com",
                    error_messages={
                        "pattern": "Invalid email format. Please provide a valid email address."
                    },
                ),
                "password": fields.String(
                    required=True, description="Password", min_length=6, max_length=25
                ),
                "phone": fields.String(
                    required=True,
                    description="Phone number",
                    min_length=1,
                    max_length=20,
                ),
                "restaurant_name": fields.String(
                    required=True, description="Restaurant name", max_length=100
                ),
                "restaurant_description": fields.String(
                    required=True, description="Restaurant description"
                ),
                "restaurant_address": fields.String(
                    required=True, description="Restaurant address", max_length=200
                ),
                "restaurant_phone": fields.String(
                    required=True, description="Restaurant phone", max_length=20
                ),
            },
        )

        self.update_customer_model = api.model(
            "UpdateUser",
            {
                "username": fields.String(
                    required=False,
                    description="Username",
                    min_length=3,
                    max_length=100,
                ),
                "phone": fields.String(
                    required=False,
                    description="Phone number",
                    min_length=1,
                    max_length=20,
                ),
                "password": fields.String(
                    required=False, description="Password", min_length=6, max_length=25
                ),
            },
        )

        self.update_staff_model = api.model(
            "UpdateStaff",
            {
                "username": fields.String(
                    required=False, description="Username", min_length=3, max_length=100
                ),
                "password": fields.String(
                    required=False, description="Password", min_length=6, max_length=25
                ),
                "phone": fields.String(
                    required=False,
                    description="Phone number",
                    min_length=1,
                    max_length=20,
                ),
                "restaurant_name": fields.String(
                    required=False, description="Restaurant name", max_length=100
                ),
                "restaurant_description": fields.String(
                    required=False, description="Restaurant description"
                ),
                "restaurant_address": fields.String(
                    required=False, description="Restaurant address", max_length=200
                ),
                "restaurant_phone": fields.String(
                    required=False, description="Restaurant phone", max_length=20
                ),
            },
        )

        ###############################################################################

        self.create_menu_category_model = api.model(
            "CreateMenuCategory",
            {
                "name": fields.String(
                    required=True, description="Category name", min_length=1
                ),
            },
        )

        self.update_menu_category_model = api.model(
            "UpdateMenuCategory",
            {
                "name": fields.String(
                    required=True, description="Category name", min_length=1
                ),
            },
        )

        self.create_menu_item_model = api.model(
            "CreateMenuItem",
            {
                "category_id": fields.Integer(required=True, description="Category ID"),
                "name": fields.String(
                    required=True, description="Menu item name", min_length=1
                ),
                "description": fields.String(
                    required=False, description="Menu item description", min_length=1
                ),
                "price": fields.Float(required=True, description="Menu item price"),
                "image": fields.String(required=False, description="Menu item image"),
            },
        )

        self.update_menu_item_model = api.model(
            "UpdateMenuItem",
            {
                "category_id": fields.Integer(
                    required=False, description="Category ID"
                ),
                "name": fields.String(
                    required=False, description="Menu item name", min_length=1
                ),
                "description": fields.String(
                    required=False, description="Menu item description", min_length=1
                ),
                "price": fields.Float(required=False, description="Menu item price"),
                "image": fields.String(required=False, description="Menu item image"),
            },
        )

        self.create_table_model = api.model(
            "CreateTable",
            {
                "name": fields.String(
                    required=True, description="Table name", min_length=1
                ),
            },
        )

        self.update_table_model = api.model(
            "UpdateTable",
            {
                "name": fields.String(
                    required=False, description="Table name", min_length=1
                ),
            },
        )

        ###############################################################################

        self.create_order_item_model = api.model(
            "CreateOrderItem",
            {
                "menu_item_id": fields.Integer(
                    required=True, description="Menu Item ID"
                ),
                "quantity": fields.Integer(
                    required=True,
                    description="Quantity",
                    min_length=1,
                ),
            },
        )

        self.create_order_model = api.model(
            "CreateOrder",
            {
                "restaurant_id": fields.Integer(
                    required=True, description="Restaurant ID"
                ),
                "table_id": fields.Integer(required=True, description="Table ID"),
                "order_items": fields.List(
                    fields.Nested(self.create_order_item_model),
                    required=True,
                    description="Order items",
                ),
            },
        )

        self.update_order_model = api.model(
            "UpdateOrder",
            {
                "status": fields.String(required=True, description="Order status"),
            },
        )


# def is_valid_email(email):
#     print("ASLDASLDASLDASLDASLDASLDASLDASLDLSAL")
#     # Define the pattern for a valid email address
#     pattern = r'^[\w\.\-]+@([\w\-]+\.)+[\w\-]{2,4}$'
#
#     # Check if the email address matches the pattern
#     if re.match(pattern, email):
#         return True
#     else:
#         return False


# def is_valid_phone_number(phone_number):
#     try:
#         parsed_number = phonenumbers.parse(phone_number)
#         return phonenumbers.is_valid_number(parsed_number)
#     except phonenumberutil.NumberParseException:
#         return False
