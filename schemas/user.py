from marshmallow import Schema, fields
from utils import hash_password

class UserSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dum_only=True)
    username = fields.String(required=True, validate=lambda x: len(x) > 6)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True, deserialize='load_password')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_admin = fields.Boolean(dump_only=True)
    is_active = fields.Boolean(dump_only=True)

    def load_password(self, value):
        return hash_password(value)