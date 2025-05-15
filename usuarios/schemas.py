from marshmallow import Schema, fields, validate, validates_schema, ValidationError



class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True, validate=validate.Length(min=1, max=100))
    senha = fields.Str(load_only=True, required=True, validate=validate.Length(min=6, max=20))
    confirmar_senha = fields.Str(load_only=True, required=True, validate=validate.Length(min=6, max=20))
    data_criacao = fields.DateTime(dump_only=True)

    @validates_schema
    def validar_forca_senha(self, dados, **kwargs):
        senha = dados.get('senha')
        confirmar_senha = dados.get('confirmar_senha')
        
        if senha != confirmar_senha:
            raise ValidationError('As senhas não coincidem.')
        
        
        if len(senha) < 6:
            raise ValidationError('A senha deve ter pelo menos 6 caracteres.')
        if not any(char.isupper() for char in senha):
            raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')
        if not any(char.islower() for char in senha):
            raise ValidationError('A senha deve conter pelo menos uma letra minúscula.')
        if not any(char.isdigit() for char in senha):
            raise ValidationError('A senha deve conter pelo menos um número.')
  
