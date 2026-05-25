from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from database import conectar, criar_tabela, sqlite3


cadastro_bp = Blueprint('cadastro', __name__)

# Função que lida com a rota da página de cadastro e insere os dados no banco de dados quando o formulário é enviado
@cadastro_bp.route('/cadastro', methods=['GET', 'POST'])

def cadastro():
    
    if request.method == 'POST':

        nome = request.form['nomeForm']
        email = request.form['emailForm']
        senha = generate_password_hash(request.form['senhaForm'])

        conn = conectar()
        c = conn.cursor()

        c.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('login.login'))
    
    return render_template('cadastro.html')