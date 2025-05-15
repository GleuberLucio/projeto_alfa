from .models import Usuario, db
from .schemas import UsuarioSchema
from marshmallow import ValidationError

usuario_schema = UsuarioSchema()

def criar_usuario(data):
    """
    Cria um novo usuário no banco de dados.
    
    :param data: Dicionário com os dados do usuário. {nome: str, email: str, senha: str}
    :type data: dict
    :return: O usuário criado.
    """
    try:
        # 1ª Validação de dados
        # Valida os dados de entrada usando o esquema definido no marshmallow
        # Isso garante que os dados estejam no formato correto e atendam às regras de validação
        dados_validos = usuario_schema.load(data)
    except ValidationError as err:
        raise ValueError(f"Dados inválidos: {err.messages}")
        
    nome = dados_validos['nome']
    email = dados_validos['email']
    senha = dados_validos['senha']
    
    # Verifica se o usuário já existe
    if Usuario.buscar_por_email(email):
        raise ValueError("Usuário já cadastrado.")
    
    # 2ª Validação de dados
    # Valida a senha e a confirmação da senha
    erros = usuario_schema.validate(dados_validos)
    if erros:
        raise ValueError(f"Dados inválidos: {erros}")

    # Após validação, cria o usuário com os dados fornecidos    
    usuario = Usuario(nome=nome, email=email)
    
    # Define a senha hash usando o método definido na classe Usuario
    usuario.definir_senha(senha)
    
    db.session.add(usuario)
    db.session.commit()
    return usuario

def listar_usuarios():
    return Usuario.listar_usuarios()

def buscar_usuario_por_email(email):
    return Usuario.buscar_por_email(email)