"""Controller de Paciente: recebe a requisição HTTP, valida e chama o Model."""
from flask import Blueprint, jsonify, request

from auth import token_obrigatorio
from models import paciente_model
from utils import erro

paciente_bp = Blueprint("paciente", __name__)

OBRIGATORIOS = ["nome", "cpf", "data_nascimento"]


def campos_ausentes(dados):
    """Lista os campos obrigatórios que não vieram (ou vieram vazios)."""
    return [c for c in OBRIGATORIOS if dados.get(c) in (None, "")]


@paciente_bp.route("/pacientes", methods=["GET"])
@token_obrigatorio
def get_all_pacientes():
    return jsonify(paciente_model.listar())


@paciente_bp.route("/pacientes/<int:id>", methods=["GET"])
@token_obrigatorio
def get_paciente_by_id(id):
    paciente = paciente_model.buscar(id)
    if paciente is None:
        return erro("Paciente não encontrado", 404)
    return jsonify(paciente)


@paciente_bp.route("/pacientes", methods=["POST"])
@token_obrigatorio
def insert_paciente():
    dados = request.get_json(silent=True) or {}
    ausentes = campos_ausentes(dados)
    if ausentes:
        return erro("Campos obrigatórios ausentes: " + ", ".join(ausentes), 400)

    novo = paciente_model.inserir(
        dados["nome"], dados["cpf"], dados["data_nascimento"], dados.get("telefone")
    )
    return jsonify(novo), 201


@paciente_bp.route("/pacientes/<int:id>", methods=["PUT"])
@token_obrigatorio
def update_paciente(id):
    dados = request.get_json(silent=True) or {}
    ausentes = campos_ausentes(dados)
    if ausentes:
        return erro("Campos obrigatórios ausentes: " + ", ".join(ausentes), 400)

    atualizado = paciente_model.atualizar(
        id, dados["nome"], dados["cpf"], dados["data_nascimento"], dados.get("telefone")
    )
    if atualizado is None:
        return erro("Paciente não encontrado", 404)
    return jsonify(atualizado)


@paciente_bp.route("/pacientes/<int:id>", methods=["DELETE"])
@token_obrigatorio
def delete_paciente(id):
    if paciente_model.buscar(id) is None:
        return erro("Paciente não encontrado", 404)

    # R6: não remove paciente que ainda tem consultas ativas
    if paciente_model.contar_consultas_ativas(id) > 0:
        return erro("Paciente possui consultas ativas e não pode ser removido", 409)

    paciente_model.remover(id)
    return jsonify({"mensagem": "Paciente removido com sucesso"})
