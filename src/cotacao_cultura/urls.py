from flask import request
from ..app import app
from .controllers import (
    list_all_cotacoes_controller,
    create_cotacao_controller,
    retrieve_cotacao_controller,
    update_cotacao_controller,
    delete_cotacao_controller,
    get_cotacao_by_cultura_controller,
    get_cotacao_atual_controller
)

@app.route("/cotacaoCultura", methods=['GET', 'POST', 'OPTIONS'])
def list_create_cotacao():
    if request.method == 'OPTIONS':
        return '', 204
    if request.method == 'GET':
        return list_all_cotacoes_controller()
    return create_cotacao_controller()

@app.route("/cotacaoCultura/<cotacao_id>", methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
def retrieve_update_delete_cotacao(cotacao_id):
    if request.method == 'OPTIONS':
        return '', 204
    if request.method == 'GET':
        return retrieve_cotacao_controller(cotacao_id)
    if request.method == 'PUT':
        return update_cotacao_controller(cotacao_id)
    if request.method == 'DELETE':
        return delete_cotacao_controller(cotacao_id)

@app.route("/cotacaoCultura/cultura/<cultura_id>", methods=['GET', 'OPTIONS'])
def get_cotacoes_by_cultura(cultura_id):
    if request.method == 'OPTIONS':
        return '', 204
    return get_cotacao_by_cultura_controller(cultura_id)

@app.route("/cotacaoCultura/cultura/<cultura_id>/atual", methods=['GET', 'OPTIONS'])
def get_cotacao_atual(cultura_id):
    if request.method == 'OPTIONS':
        return '', 204
    return get_cotacao_atual_controller(cultura_id)

# Alias para compatibilidade com frontend
@app.route("/cotacaoCultura/atual/<cultura_id>", methods=['GET', 'OPTIONS'])
def get_cotacao_atual_alias(cultura_id):
    if request.method == 'OPTIONS':
        return '', 204
    return get_cotacao_atual_controller(cultura_id)