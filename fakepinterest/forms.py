from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from fakepinterest.models import Usuario


class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=20)])
    botao_confirmacao = SubmitField("Fazer login")
    botao_cadastro = SubmitField("Ainda não tem conta? Cadastre-se")


class FormCriarConta(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField(
        "Nome de usuário", validators=[DataRequired(), Length(min=2, max=20)]
    )
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=20)])
    confirmar_senha = PasswordField(
        "Confirmar senha", validators=[DataRequired(), EqualTo("senha")]
    )
    botao_confirmacao = SubmitField("Criar conta")

    def validate_email(self):
        usuario = Usuario.query.filter_by(email=self.email.data).first()
        if usuario:
            raise ValidationError(
                "Email já cadastrado. Cadastre outro email ou faça login para continuar."
            )
