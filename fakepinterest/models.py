from fakepinterest import database, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id_usuario): 
    return Usuario.query.get(int(id_usuario))
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    senha = database.Column(database.String(60), nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String(1024), default="default.png", nullable=False)
    data_criacao = database.Column(
        database.DateTime, 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc)
    )
    id_usuario = database.Column(
        database.Integer, database.ForeignKey("usuario.id"), nullable=False
    )
