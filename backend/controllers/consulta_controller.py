"""Controller de Consulta: recebe a requisição HTTP, valida e chama o Model."""
from flask import Blueprint, jsonify, request

from auth import token_obrigatorio
from models import consulta_model, paciente_model
from utils import erro

consulta_bp = Blueprint("consulta", __name__)

OBRIGATORIOS = ["paciente_id", "data_consulta", "descricao", "valor"]


def validar(dados):
    """Devolve (mensagem, status) se algo estiver errado, ou None se estiver tudo certo."""
    ausentes = [c for c in OBRIGATORIOS if dados.get(c) in (None, "")]
    if ausentes:
        return "Campos obrigatórios ausentes: " + ", ".join(ausentes), 400

    try:
        valor = float(dados["valor"])
    except (TypeError, ValueError):
        return "O campo valor deve ser numérico", 400
    if valor < 0:
        return "O campo valor não pode ser negativo", 400

    # R4: o paciente precisa existir e não estar removido
    if paciente_model.buscar(dados["paciente_id"]) is None:
        return "Paciente não encontrado", 404

    return None


@consulta_bp.route("/consultas", methods=["GET"])
@token_obrigatorio
def get_all_consultas():
    return jsonify(consulta_model.listar())


@consulta_bp.route("/consultas/<int:id>", methods=["GET"])
@token_obrigatorio
def get_consulta_by_id(id):
    consulta = consulta_model.buscar(id)
    if consulta is None:
        return erro("Consulta não encontrada", 404)
    return jsonify(consulta)


@consulta_bp.route("/consultas", methods=["POST"])
@token_obrigatorio
def insert_consulta():
    dados = request.get_json(silent=True) or {}
    problema = validar(dados)
    if problema:
        return erro(*problema)

    nova = consulta_model.inserir(
        dados["paciente_id"], dados["data_consulta"], dados["descricao"], dados["valor"]
    )
    return jsonify(nova), 201


@consulta_bp.route("/consultas/<int:id>", methods=["PUT"])
@token_obrigatorio
def update_consulta(id):
    dados = request.get_json(silent=True) or {}
    problema = validar(dados)
    if problema:
        return erro(*problema)

    atualizada = consulta_model.atualizar(
        id, dados["paciente_id"], dados["data_consulta"], dados["descricao"], dados["valor"]
    )
    if atualizada is None:
        return erro("Consulta não encontrada", 404)
    return jsonify(atualizada)


@consulta_bp.route("/consultas/<int:id>", methods=["DELETE"])
@token_obrigatorio
def delete_consulta(id):
    if consulta_model.remover(id) == 0:
        return erro("Consulta não encontrada", 404)
    return jsonify({"mensagem": "Consulta removida com sucesso"})
