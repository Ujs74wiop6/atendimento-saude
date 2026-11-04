from db import executar

SELECT_BASE = (
    "SELECT c.id, c.paciente_id, p.nome AS paciente_nome, "
    "c.data_consulta, c.descricao, c.valor, c.removido "
    "FROM consulta c JOIN paciente p ON p.id = c.paciente_id "
)


def listar():
    return executar(
        SELECT_BASE + "WHERE c.removido = false ORDER BY c.id",
        retorno="todos",
    )


def buscar(id):
    return executar(
        SELECT_BASE + "WHERE c.id = %s AND c.removido = false",
        (id,),
        "um",
    )


def inserir(paciente_id, data_consulta, descricao, valor):
    novo = executar(
        "INSERT INTO consulta (paciente_id, data_consulta, descricao, valor) "
        "VALUES (%s, %s, %s, %s) RETURNING id",
        (paciente_id, data_consulta, descricao, valor),
        "um",
    )
    return buscar(novo["id"])  # busca de novo para vir com o nome do paciente


def atualizar(id, paciente_id, data_consulta, descricao, valor):
    linhas = executar(
        "UPDATE consulta SET paciente_id = %s, data_consulta = %s, "
        "descricao = %s, valor = %s WHERE id = %s AND removido = false",
        (paciente_id, data_consulta, descricao, valor, id),
    )
    if linhas == 0:
        return None  # id não existe
    return buscar(id)


def remover(id):
    # R2: soft delete
    return executar(
        "UPDATE consulta SET removido = true WHERE id = %s AND removido = false",
        (id,),
    )
