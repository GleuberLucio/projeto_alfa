from flask import Blueprint, request, jsonify
from .controllers import autenticar_usuario, gerar_token_recuperacao
from models.usuarios.models import Usuario
from .email_utils import enviar_email_recuperacao

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
    
@auth_bp.route('/recuperar_senha', methods=['POST'])
def recuperar_senha():
    """
    Rota para recuperação de senha.
    Recebe um JSON com 'email' e envia um email de recuperação.
    """
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({"msg": "Email é obrigatório."}), 400

    email = data['email']
    
    usuario = Usuario.buscar_por_email(email)
    if not usuario:
        return jsonify({"msg": "Email não encontrado."}), 404
    
    token_recuperacao = gerar_token_recuperacao(usuario.id)
    link_recuperacao = f"http://localhost:8000/recuperar_senha?token={token_recuperacao}"
    
    if enviar_email_recuperacao(
        email_destino=email,
        assunto="Recuperação de Senha",
        corpo=f"Olá {usuario.nome}," + 
        "\nRecebemos uma solicitação para redefinir sua senha.\n" + 
        "\nSe você não solicitou essa alteração, ignore este email.\n" + 
        f"\nClique no link para redefinir sua senha: {link_recuperacao}" + 
        "\n\n*Valido por 15 minutos."
        ):
    
        return jsonify({"msg": "Email de recuperação enviado."}), 200

    return jsonify({"msg": "Erro ao enviar email de recuperação."}), 500