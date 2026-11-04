from db import executar

COLUNAS = "id, nome, cpf, data_nascimento, telefone, removido"


def listar():
    # R1: só traz quem NÃO foi removido
    return executar(
        f"SELECT {COLUNAS} FROM paciente WHERE removido = false ORDER BY id",
        retorno="todos",
    )


def buscar(id):
    return executar(
        f"SELECT {COLUNAS} FROM paciente WHERE id = %s AND removido = false",
        (id,),
        "um",
    )


def inserir(nome, cpf, data_nascimento, telefone):
    return executar(
        "INSERT INTO paciente (nome, cpf, data_nascimento, telefone) "
        f"VALUES (%s, %s, %s, %s) RETURNING {COLUNAS}",
        (nome, cpf, data_nascimento, telefone),
        "um",
    )


def atualizar(id, nome, cpf, data_nascimento, telefone):
    # Devolve None se o id não existe (ou já foi removido)
    return executar(
        "UPDATE paciente SET nome = %s, cpf = %s, data_nascimento = %s, telefone = %s "
        f"WHERE id = %s AND removido = false RETURNING {COLUNAS}",
        (nome, cpf, data_nascimento, telefone, id),
        "um",
    )


def remover(id):
    # R2: soft delete. Não apaga a linha, só marca como removida.
    # Devolve quantas linhas foram alteradas (0 = id não existe).
    return executar(
        "UPDATE paciente SET removido = true WHERE id = %s AND removido = false",
        (id,),
    )


def contar_consultas_ativas(id):
    resultado = executar(
        "SELECT COUNT(*) AS total FROM consulta "
        "WHERE paciente_id = %s AND removido = false",
        (id,),
        "um",
    )
    return resultado["total"]
