from flask import request

from ..app import app
from .controllers import list_all_horasFuncionario_controller, create_horasFuncionario_controller, retrieve_horasFuncionario_controller, update_horasFuncionario_controller, delete_horasFuncionario_controller

@app.route("/horasFuncionario", methods=['GET', 'POST'])
def list_create_horasFuncionario():
    if request.method == 'GET': return list_all_horasFuncionario_controller()
    if request.method == 'POST': return create_horasFuncionario_controller()
    else: return 'Method is Not Allowed'

@app.route("/horasFuncionario/<horasFuncionario_id>", methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_horasFuncionario(horasFuncionario_id):
    if request.method == 'GET': return retrieve_horasFuncionario_controller(horasFuncionario_id)
    if request.method == 'PUT': return update_horasFuncionario_controller(horasFuncionario_id)
    if request.method == 'DELETE': return delete_horasFuncionario_controller(horasFuncionario_id)
    else: return 'Method is Not Allowed'