from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'taskcraft_secret_key'

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

def conectar():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar a tabela no banco de dados
def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nome TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  senha TEXT NOT NULL)''')
    conn.commit()
    conn.close()

criar_tabela()

# Rota para a página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])

# Função que lida com a rota da página de cadastro e insere os dados no banco de dados quando o formulário é enviado
def cadastro():
    if request.method == 'POST':
        conn = conectar()
        c = conn.cursor()
        senha = request.form['senhaForm']
        senha_hash = generate_password_hash(senha)
        try:
            c.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (request.form['nomeForm'], request.form['emailForm'], senha_hash))
            conn.commit()
            session['usuario'] = request.form['nomeForm']
            return redirect(url_for('dashboard'))
        except sqlite3.IntegrityError:
            return render_template('cadastro.html', erro="Email já cadastrado.")
        finally:
            conn.close()
    return render_template('cadastro.html')

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])

# Função que lida com a rota da página de login, verifica as credenciais do usuário e inicia a sessão se o login for bem-sucedido
def login():
    if request.method == 'POST':
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE email = ?", (request.form['emailForm'],))
        user = c.fetchone()
        conn.close()
        if user:
            if check_password_hash(user['senha'], request.form['senhaForm']):
                session['usuario'] = user['nome']
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', erro="Senha incorreta.")
        else:
            return render_template('login.html', erro="Email não encontrado.")
    return render_template('login.html')

# Rota para a página de dashboard (após login bem-sucedido)
@app.route('/dashboard')

# Função que lida com a rota do dashboard e exibe uma mensagem de boas-vindas ao usuário logado
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'])
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
