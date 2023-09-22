from marshmallow import Schema, fields


class CreateUserRequest(Schema):
    name = fields.Str()
    surname = fields.Str()
    email = fields.Str()
    eth_address = fields.Str()
    password = fields.Str()


class CreateTokenRequest(Schema):
    email = fields.Str()
    password = fields.Str()


class GetUserResponse(Schema):
    name = fields.Str()
    surname = fields.Str()
    email = fields.Str()
    eth_address = fields.Str()
