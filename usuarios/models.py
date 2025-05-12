from flask_sqlalchemy import SQLAlchemy

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
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'