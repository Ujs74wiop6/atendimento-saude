import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import Blueprint, jsonify, request

from db import executar
from utils import erro

auth_bp = Blueprint("auth", __name__)

# Chave usada para assinar o token. Vem do docker-compose.yml.
JWT_SECRET = os.getenv("JWT_SECRET", "9as1%12#xz0#@")


@auth_bp.route("/login", methods=["POST"])
def login():
    """POST /login: confere usuário e senha e devolve um token JWT."""
    dados = request.get_json(silent=True) or {}

    usuario = executar(
        "SELECT id, login FROM usuario "
        "WHERE login = %s AND senha = %s AND removido = false",
        (dados.get("login"), dados.get("senha")),
        "um",
    )
    if usuario is None:
        return erro("Login ou senha inválidos", 401)

    # O token carrega o id do usuário e a data de validade (1 hora)
    token = jwt.encode(
        {
            "id": usuario["id"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        JWT_SECRET,
        algorithm="HS256",
    )
    return jsonify({"token": token, "usuario": usuario})


def token_obrigatorio(funcao):
    """Decorator: protege uma rota. Só executa a rota se o token for válido."""

    @wraps(funcao)
    def verificar(*args, **kwargs):
        cabecalho = request.headers.get("Authorization", "")
        if not cabecalho.startswith("Bearer "):
            return erro("Token não informado", 401)

        token = cabecalho[len("Bearer "):]
        try:
            # Confere a assinatura e a validade do token
            jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return erro("Token inválido ou expirado", 401)

        return funcao(*args, **kwargs)

    return verificar
