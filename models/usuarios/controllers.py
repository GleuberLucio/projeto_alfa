from .models import Usuario
from extensions import db
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

def buscar_usuario_por_id(id):
    return Usuario.buscar_por_id(id)

def redefinir_senha(usuario, nova_senha, confirmar_senha):
    """
    Redefine a senha do usuário.
    
    :param usuario: O usuário cujo a senha será redefinida.
    :type usuario: Usuario
    :param nova_senha: A nova senha a ser definida.
    :type nova_senha: str
    """
    try:
        erros = usuario_schema.validate({'nome': usuario.nome, 'email': usuario.email, 'senha': nova_senha, 'confirmar_senha': confirmar_senha})
        
        if erros:
            raise ValueError(f"Dados inválidos: {erros}")

        usuario.definir_senha(nova_senha)
        db.session.commit()
    
    except Exception as err:
        db.session.rollback()
        raise ValueError(f"Erro ao redefinir senha: {err}")
    

def atualizar_usuario(usuario, data):
    """
    Atualiza os dados do usuário.
    
    :param usuario: O usuário a ser atualizado.
    :type usuario: Usuario
    :param data: Dicionário com os novos dados do usuário. {nome: str, email: str, senha: str}
    :type data: dict
    """
    try:
        # Valida os dados de entrada usando o esquema definido no marshmallow
        dados_validos = usuario_schema.load(data)
        
        erros = usuario_schema.validate(dados_validos)
        if erros:
            raise ValueError(f"Dados inválidos: {erros}")
        
        # Atualiza os atributos do usuário
        usuario.nome = dados_validos['nome']
        usuario.email = dados_validos['email']
        
        if 'senha' in dados_validos and 'confirmar_senha' in dados_validos:
            usuario.definir_senha(dados_validos['senha'])
        
        db.session.commit()
        return usuario
    
    except ValidationError as err:
        raise ValueError(f"Dados inválidos: {err.messages}")
    
def excluir_usuario(usuario):
    """
    Exclui um usuário do banco de dados.
    
    :param usuario: O usuário a ser excluído.
    :type usuario: Usuario
    """
    try:
        db.session.delete(usuario)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        raise ValueError(f"Erro ao excluir usuário: {err}")