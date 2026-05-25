from flask import Flask

from routes.home import home_bp
from routes.login import login_bp
from routes.cadastro import cadastro_bp
from routes.dashboard import dashboard_bp

from database import criar_tabela

app = Flask(__name__)

app.secret_key = 'taskcraft_secret_key'


app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(cadastro_bp)
app.register_blueprint(dashboard_bp)

criar_tabela()

if __name__ == "__main__":
    app.run(debug=True)