from flask import Blueprint, request, jsonify
from .controllers import criar_usuario, buscar_usuario_por_email, listar_usuarios

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