from marshmallow import Schema, fields

from marshmallow.validate import Length, Range, URL


class AccountSchema(Schema):
    access_token = fields.Str(required=True, validate=Length(40))


class SiteSchema(Schema):
    url = fields.Str(required=True, validate=URL())
    site_key = fields.Str(required=True, validate=Length(32))
