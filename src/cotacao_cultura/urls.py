from flask import request

from ..app import app
from .controllers import list_all_cotacaoCultura_controller, create_cotacaoCultura_controller, retrieve_cotacaoCultura_controller, update_cotacaoCultura_controller, delete_cotacaoCultura_controller

@app.route("/cotacaoCultura", methods=['GET', 'POST'])
def list_create_cotacaoCultura():
    if request.method == 'GET': return list_all_cotacaoCultura_controller()
    if request.method == 'POST': return create_cotacaoCultura_controller()
    else: return 'Method is Not Allowed'

@app.route("/cotacaoCultura/<cotacaoCultura_id>", methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_cotacaoCultura(cotacaoCultura_id):
    if request.method == 'GET': return retrieve_cotacaoCultura_controller(cotacaoCultura_id)
    if request.method == 'PUT': return update_cotacaoCultura_controller(cotacaoCultura_id)
    if request.method == 'DELETE': return delete_cotacaoCultura_controller(cotacaoCultura_id)
    else: return 'Method is Not Allowed'