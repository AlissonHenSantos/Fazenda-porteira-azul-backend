from flask import request

from ..app import app
from .controllers import list_all_maquina_controller, create_maquina_controller, retrieve_maquina_controller, update_maquina_controller, delete_maquina_controller

@app.route("/maquinario", methods=['GET', 'POST'])
def list_create_maquina():
    if request.method == 'GET': return list_all_maquina_controller()
    if request.method == 'POST': return create_maquina_controller()
    else: return 'Method is Not Allowed'

@app.route("/maquinario/<maquina_id>", methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_maquina(maquina_id):
    if request.method == 'GET': return retrieve_maquina_controller(maquina_id)
    if request.method == 'PUT': return update_maquina_controller(maquina_id)
    if request.method == 'DELETE': return delete_maquina_controller(maquina_id)
    else: return 'Method is Not Allowed'