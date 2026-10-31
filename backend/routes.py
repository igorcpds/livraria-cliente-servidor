from flask import Blueprint, jsonify, request
from negocio import LivrariaNegocio

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/livros", methods=["GET"])
def listar_livros():
    termo = request.args.get("q", "")
    return jsonify(LivrariaNegocio.consultar_catalogo(termo)), 200

@api_bp.route("/carrinho", methods=["GET"])
def ver_carrinho():
    return jsonify(LivrariaNegocio.obter_estado_carrinho()), 200

@api_bp.route("/carrinho/adicionar", methods=["POST"])
def adicionar_id():
    dados = request.get_json() or {}
    try:
        estado = LivrariaNegocio.adicionar_por_id(int(dados.get("livro_id", 0)))
        return jsonify(estado), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@api_bp.route("/carrinho/scan", methods=["POST"])
def scan_isbn():
    dados = request.get_json() or {}
    try:
        res = LivrariaNegocio.adicionar_por_isbn(dados.get("isbn", ""))
        return jsonify(res), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404

@api_bp.route("/carrinho/remover/<int:index>", methods=["DELETE"])
def remover_item(index):
    return jsonify(LivrariaNegocio.remover_item(index)), 200

@api_bp.route("/checkout/pix", methods=["POST"])
def checkout_pix():
    dados = request.get_json() or {}
    try:
        recibo = LivrariaNegocio.finalizar_checkout_pix(dados.get("cliente", "Cliente"))
        return jsonify(recibo), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
