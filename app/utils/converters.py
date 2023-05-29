from flask_restx import fields

def cerberus_to_flaskrestx(schema, api, model_name=None):
    mapping = {
        'string': fields.String,
        'integer': fields.Integer,
        'float': fields.Float,
        'list': fields.List,
        'dict': fields.Nested
    }

    output = {}

    for field, rules in schema.items():
        field_type = rules.get('type')

        if field_type not in mapping:
            raise ValueError(f'Cannot convert type {field_type} to Flask-RESTX type')

        if field_type == 'list':
            # If the field is a list, we need to get the schema for the items
            items_schema = rules.get('schema', {})
            if items_schema.get('type') == 'dict':
                # If the items are dictionaries, we use Nested
                field_instance = fields.List(fields.Nested(cerberus_to_flaskrestx(items_schema['schema'], api)))
            else:
                # Otherwise, we use the corresponding field type
                field_instance = fields.List(mapping[items_schema.get('type')](description=field))
        elif field_type == 'dict':
            # If the field is a dict, we need to get its schema
            field_instance = fields.Nested(cerberus_to_flaskrestx(rules['schema'], api))
        else:
            field_instance = mapping[field_type](required=rules.get('required', False),
                                                 min_length=rules.get('minlength', None),
                                                 max_length=rules.get('maxlength', None),
                                                 description=field)

        output[field] = field_instance

    return api.model(model_name, output)  # model creation with a unique name based on schema class
