from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())

    @classmethod
    def buscar_por_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def listar_usuarios(cls):
        return cls.query.all()
    
    @classmethod
    def buscar_por_id(cls, id):
        return cls.query.get(id)
    
    def definir_senha(self, senha):
        """Criptografa e guarda o hash da senha"""
        self.senha = sha256.hash(senha)
        
    def verificar_senha(self, senha):
        """Compara a senha digitada com a senha salva"""
        return sha256.verify(senha, self.senha)
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'