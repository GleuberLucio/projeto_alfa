from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .controllers import criar_usuario, buscar_usuario_por_email, listar_usuarios
from auth.controllers import renovar_token

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')

@usuarios_bp.route('/', methods=['POST'])
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

@usuarios_bp.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def rota_refresh():
    """Rota para atualizar o token de acesso."""
    usuario_id = get_jwt_identity()
    access_token = renovar_token(usuario_id)
    return jsonify({
        'access_token': access_token,
        'message': 'Rota protegida acessada com sucesso!'
    }), 200