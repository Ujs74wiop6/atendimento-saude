from datetime import date, datetime
from decimal import Decimal

from flask import jsonify


def erro(mensagem, status):
    """Resposta de erro padrão da API: {"erro": "..."} + código HTTP."""
    return jsonify({"erro": mensagem}), status


def limpar(linha):
    """Converte os tipos do banco para tipos que o JSON entende.
    - date/datetime -> texto no formato AAAA-MM-DD
    - Decimal (NUMERIC) -> número (float)
    """
    if linha is None:
        return None
    resultado = {}
    for chave, valor in linha.items():
        if isinstance(valor, (date, datetime)):
            valor = valor.isoformat()
        elif isinstance(valor, Decimal):
            valor = float(valor)
        resultado[chave] = valor
    return resultado
