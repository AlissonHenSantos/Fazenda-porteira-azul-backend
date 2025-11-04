from flask import request

from ..app import app
from .controllers import list_all_funcionario_controller, create_funcionario_controller, retrieve_funcionario_controller, update_funcionario_controller, delete_funcionario_controller

@app.route("/funcionario", methods=['GET', 'POST'])
def list_create_funcionario():
    if request.method == 'GET': return list_all_funcionario_controller()
    if request.method == 'POST': return create_funcionario_controller()
    else: return 'Method is Not Allowed'

@app.route("/funcionario/<funcionario_id>", methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_funcionario(funcionario_id):
    if request.method == 'GET': return retrieve_funcionario_controller(funcionario_id)
    if request.method == 'PUT': return update_funcionario_controller(funcionario_id)
    if request.method == 'DELETE': return delete_funcionario_controller(funcionario_id)
    else: return 'Method is Not Allowed'