from flask import Blueprint, request, jsonify
from .controllers import autenticar_usuario

# Criando o Blueprint para autenticação de usuários
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Rota para autenticação de usuários.
    Recebe um JSON com 'email' e 'senha' e retorna um token JWT se as credenciais forem válidas.
    """
    data = request.get_json()
    
    if not data or 'email' not in data or 'senha' not in data:
        return jsonify({"msg": "Email e senha são obrigatórios."}), 400

    email = data['email']
    senha = data['senha']

    try:
        tokens = autenticar_usuario(email, senha)
        acess_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        
        return jsonify({"acess_token": acess_token,
                        "refresh_token": refresh_token
                        }), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 401