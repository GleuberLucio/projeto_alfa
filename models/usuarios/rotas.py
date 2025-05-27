from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from .controllers import criar_usuario, buscar_usuario_por_email, listar_usuarios, redefinir_senha, buscar_usuario_por_id, atualizar_usuario, excluir_usuario
from auth.controllers import renovar_token

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')

@usuarios_bp.route('/cadastro', methods=['POST'])
def rota_criar_usuario():
    dados = request.get_json()
    try:
        usuario = criar_usuario(dados)
        return jsonify({'message': f'Cadastro de {usuario.email} realizado com sucesso.'}), 201
    except ValueError as e:
        return jsonify({'erros': e.args[0]}), 400

@usuarios_bp.route('/', methods=['GET'])
def rota_listar_usuarios():
    usuarios = listar_usuarios()
    lista = [{'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email} for usuario in usuarios]
    
    return jsonify(lista), 200

@usuarios_bp.route('/<string:email>', methods=['GET'])
def rota_buscar_usuario_por_email(email):
    usuario = buscar_usuario_por_email(email)
    if usuario:
        response = {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': 'Usuário não encontrado.'}), 404
    
@usuarios_bp.route('/protegido', methods=['GET'])
@jwt_required()
def rota_protegido():
    return jsonify({'message': 'Rota protegida acessada com sucesso!'}), 200

@usuarios_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def rota_refresh():
    """Rota para atualizar o token de acesso."""
    usuario_id = get_jwt_identity()
    access_token = renovar_token(usuario_id)
    return jsonify({
        'access_token': access_token,
        'message': 'Rota protegida acessada com sucesso!'
    }), 200
    
@usuarios_bp.route('/recuperar_senha', methods=['POST'])
@jwt_required()
def rota_recuperar_senha():
    """
    Rota para recuperação de senha.
    Recebe um JSON com 'email' e envia um email de recuperação.
    """
    claims = get_jwt()
    
    if not claims.get('recuperacao'):
        return jsonify({"msg": "Token inválido para esta operação."}), 403
    
    dados = request.get_json()
    nova_senha = dados.get('nova_senha')
    confirmar_senha = dados.get('confirmar_senha')
    
    if nova_senha != confirmar_senha:
        return jsonify({"msg": "As senhas não coincidem."}), 400
    
    usuario_id = get_jwt_identity()
    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        return jsonify({"msg": "Usuário não encontrado."}), 404
    
    redefinir_senha(usuario, nova_senha, confirmar_senha)
    
    return jsonify({"msg": f"{usuario.nome}, A recuperação de senha foi realizada com sucesso."}), 200

@usuarios_bp.route('/atualizar', methods=['PUT'])
@jwt_required()
def rota_atualizar_usuario():
    """
    Rota para atualizar dados do usuário.
    Recebe um JSON com 'nome', 'email', 'senha' e 'confirmar_senha'.
    """
    dados = request.get_json()
    nova_senha = dados.get('senha')
    confirmar_senha = dados.get('confirmar_senha')
    
    if nova_senha != confirmar_senha:
        return jsonify({"msg": "As senhas não coincidem."}), 400
    
    usuario_id = get_jwt_identity()
    usuario = buscar_usuario_por_id(usuario_id)
    
    if not usuario:
        return jsonify({"msg": "Usuário não encontrado."}), 404
    
    atualizar_usuario(usuario, dados)
    
    return jsonify({"msg": f"{usuario.nome}, atualização concluída."}), 200

@usuarios_bp.route('/excluir', methods=['DELETE'])
@jwt_required()
def rota_excluir_usuario():
    """
    Rota para excluir o usuário autenticado.
    """
    usuario_id = get_jwt_identity()
    usuario = buscar_usuario_por_id(usuario_id)
    
    if not usuario:
        return jsonify({"msg": "Usuário não encontrado."}), 404
    
    excluir_usuario(usuario)
    
    return jsonify({"msg": f"{usuario.nome}, sua conta foi excluída com sucesso."}), 200