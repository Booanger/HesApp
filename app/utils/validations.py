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
