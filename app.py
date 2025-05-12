from flask import Flask
from config import Config
from usuarios.models import db
from flask_migrate import Migrate
from usuarios.rotas import usuarios_bp


app = Flask(__name__)

migrate = Migrate()

# Configuração do banco de dados
app.config.from_object(Config)

# Inicializa o banco de dados
db.init_app(app)
migrate.init_app(app, db)

# Registra o blueprints (rotas)
app.register_blueprint(usuarios_bp)

# Cria o banco de dados
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=8000)