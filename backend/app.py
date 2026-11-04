import psycopg2
from flask import Flask
from flask_cors import CORS

from auth import auth_bp
from controllers.consulta_controller import consulta_bp
from controllers.paciente_controller import paciente_bp
from utils import erro

app = Flask(__name__)

# autorizando o recebimento de requisição vindo da porta 3000 (front)
CORS(app, origins=["http://localhost:3000"])

# Registra as rotas de cada módulo
app.register_blueprint(auth_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(consulta_bp)


# ---- Tratamento central de erros do banco ---- 

@app.errorhandler(psycopg2.errors.UniqueViolation)
def erro_duplicado(e):
    return erro("CPF já cadastrado", 409)  # R3

@app.errorhandler(psycopg2.errors.CheckViolation)
@app.errorhandler(psycopg2.DataError)
def erro_dado_invalido(e):
    # Ex.: data em formato errado, texto no lugar de número
    return erro("Dado inválido. Confira os valores enviados", 400)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
