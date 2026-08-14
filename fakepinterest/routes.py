from flask import render_template, url_for, redirect
from fakepinterest import app, bcrypt, database
from flask_login import current_user, login_required, login_user, logout_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto
from werkzeug.utils import secure_filename
import os


@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=formlogin)


@app.route("/criar_conta", methods=["GET", "POST"])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senhasenhacriptografada = bcrypt.generate_password_hash(
            form_criarconta.senha.data
        ).decode("utf-8")
        usuario = Usuario(
            email=form_criarconta.email.data,
            username=form_criarconta.username.data,
            senha=senhasenhacriptografada,
        )
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criar_conta.html", form=form_criarconta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == current_user.id:
        formuploadfotos = FormFoto()
        if formuploadfotos.validate_on_submit(): 
            arquivo = formuploadfotos.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho_arquivo = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                                      app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho_arquivo)            

            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            return redirect(url_for("perfil", id_usuario=current_user.id))
        return render_template(
            "perfil.html", usuario=current_user, form=formuploadfotos
        )
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))
