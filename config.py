
class Config:
    database_name = 'database'
    # Configuração do banco de dados (SQLite)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{database_name}.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'minha_chave_super_secreta'