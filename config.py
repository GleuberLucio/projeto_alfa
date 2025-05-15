
class Config:
    
    # Configuração do banco de dados (SQLite)
    database_name = 'database'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{database_name}.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'minha_chave_super_secreta'
    
    # Configuração do Flask-Mail
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 587
    MAIL_USERNAME = '85e618e597d640'
    MAIL_PASSWORD = '84264ae75c2fcf'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'Login App', 'Teste com SandBox Mailtrap'