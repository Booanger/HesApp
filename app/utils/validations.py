from cerberus import Validator

def validate_json_data(data, schema):
    if not isinstance(data, dict):
        return False, {"msg": "Data is not a valid JSON object"}

    if not schema.validate(data):
        return False, {"msg": "Bad request parameters", "errors": schema.errors}

    return True, data

register_validator = Validator({
    'first_name': {'type': 'string', 'minlength': 1, 'required': True},
    'last_name': {'type': 'string', 'minlength': 1, 'required': True},
    'email': {'type': 'string', 'minlength': 5, 'required': True},
    'password': {'type': 'string', 'minlength': 5, 'required': True},
    'phone': {'type': 'string', 'minlength': 1, 'required': True},
    'role': {'type': 'string', 'allowed': ['customer', 'staff'], 'required': True},
})

login_validator = Validator({
    'email': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 120},
    'password': {'type': 'string', 'required': True, 'empty': False, 'minlength': 8},
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

# You can add more validators here for other routes or data structures
