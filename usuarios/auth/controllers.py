from usuarios.models import Usuario
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from flask import jsonify


def autenticar_usuario(email, senha):
    """Autentica um usuário e gera tokens de acesso e atualização."""
    
    # Verifica se o usuário existe e se a senha está correta
    usuario = Usuario.buscar_por_email(email)
    if usuario and usuario.verificar_senha(senha):
        
        # Gerar tokens de acesso e atualização
        access_token = create_access_token(identity=str(usuario.id), expires_delta=timedelta(hours=1))
        refresh_token = create_refresh_token(identity=str(usuario.id), expires_delta=timedelta(hours=1))
        
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    else:
        raise ValueError("Email ou senha inválidos.")

def renovar_token(usuario_id):
    """Renova o token de acesso."""
    
    # Gera um novo token de acesso
    access_token = create_access_token(identity=usuario_id, expires_delta=timedelta(hours=1))
    
    return jsonify({
        "access_token": access_token
    }), 200