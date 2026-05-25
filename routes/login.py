from flask import Blueprint, render_template, request, session, redirect, url_for

from werkzeug.security import check_password_hash
from database import conectar

login_bp = Blueprint("login", __name__)

# Função que lida com a rota da página de login, verifica as credenciais do usuário e inicia a sessão se o login for bem-sucedido
@login_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        conn = conectar()
        c = conn.cursor()

        c.execute(
            "SELECT * FROM usuarios WHERE email = ?",
                  (request.form['emailForm'],)
        )

        user = c.fetchone()

        conn.close()

        if user:
            if check_password_hash(user['senha'], request.form['senhaForm']):
                session['usuario'] = user['nome']
                return redirect(url_for('dashboard.dashboard'))
            else:
                return render_template('login.html', erro="Senha incorreta.")
            
        else:
            return render_template('login.html', erro="Email não encontrado.")
        
    return render_template('login.html')