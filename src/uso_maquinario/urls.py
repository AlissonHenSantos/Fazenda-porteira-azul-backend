from flask import request

from ..app import app
from .controllers import list_all_usoMaquinario_controller, create_usoMaquinario_controller, retrieve_usoMaquinario_controller, update_usoMaquinario_controller, delete_usoMaquinario_controller

@app.route("/usoMaquinario", methods=['GET', 'POST'])
def list_create_usoMaquinario():
    if request.method == 'GET': return list_all_usoMaquinario_controller()
    if request.method == 'POST': return create_usoMaquinario_controller()
    else: return 'Method is Not Allowed'

@app.route("/usoMaquinario/<usoMaquinario_id>", methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_usoMaquinario(usoMaquinario_id):
    if request.method == 'GET': return retrieve_usoMaquinario_controller(usoMaquinario_id)
    if request.method == 'PUT': return update_usoMaquinario_controller(usoMaquinario_id)
    if request.method == 'DELETE': return delete_usoMaquinario_controller(usoMaquinario_id)
    else: return 'Method is Not Allowed'