import os

import psycopg2
import psycopg2.extras

from utils import limpar


def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "atendimento"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def executar(sql, parametros=(), retorno=None):
    conexao = conectar()
    try:
        with conexao:  # confirma (commit) no fim, ou desfaz (rollback) se der erro
            with conexao.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql, parametros)
                if retorno == "todos":
                    return [limpar(linha) for linha in cursor.fetchall()]
                if retorno == "um":
                    return limpar(cursor.fetchone())
                return cursor.rowcount
    finally:
        conexao.close()
