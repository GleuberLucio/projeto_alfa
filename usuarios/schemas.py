from marshmallow import Schema, fields, validate, ValidationError


class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True, validate=validate.Length(min=1, max=100))
    senha = fields.Str(load_only=True, required=True, validate=validate.Length(min=6, max=12))
    data_criacao = fields.DateTime(dump_only=True)

