from flask_mail import Message
from extensions import mail

def enviar_email_recuperacao(email_destino, assunto, corpo):
    from app import mail  # Importando a instância do Flask-Mail
    msg = Message(
        subject=assunto,
        recipients=[email_destino],
        body=corpo
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False