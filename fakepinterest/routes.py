from flask import render_template, url_for
from fakepinterest import app
from flask_login import current_user, login_required
from fakepinterest.forms import FormLogin, FormCriarConta

@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()
    return render_template('homepage.html', form=formlogin)

@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    formcriarconta = FormCriarConta()
    return render_template('criar_conta.html', form=formcriarconta)  

@app.route('/login')
def login():
    formlogin = FormLogin()
    return render_template('login.html', form=formlogin)

@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):    
    return render_template('perfil.html', usuario=usuario)