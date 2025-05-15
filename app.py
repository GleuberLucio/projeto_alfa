import sys
import os
from flask import Flask
from config import Config

from extensions import db, migrate, mail
from flask_jwt_extended import JWTManager

# Adiciona o diretório do projeto ao sys.path para garantir que os pacotes sejam encontrados
sys.path.append(os.path.join(os.path.dirname(__file__), 'usuarios'))

from models.usuarios.models import db
from models.usuarios.rotas import usuarios_bp
from auth.rotas import auth_bp


app = Flask(__name__)
app.config.from_object(Config)

# Inicializa as extensões
db.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)
JWTManager(app)


# Registra o blueprints (rotas)
app.register_blueprint(usuarios_bp)
app.register_blueprint(auth_bp)


# Cria o banco de dados
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=8000)