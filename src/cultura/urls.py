from flask import request

from ..app import app
from .controllers import list_all_cultura_controller, create_cultura_controller, retrieve_cultura_controller, update_cultura_controller, delete_cultura_controller

@app.route("/cultura", methods=['GET', 'POST'])
def list_create_cultura():
    if request.method == 'GET': return list_all_cultura_controller()
    if request.method == 'POST': return create_cultura_controller()
    else: return 'Method is Not Allowed'

@app.route("/cultura/<cultura_id>", methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_cultura(cultura_id):
    if request.method == 'GET': return retrieve_cultura_controller(cultura_id)
    if request.method == 'PUT': return update_cultura_controller(cultura_id)
    if request.method == 'DELETE': return delete_cultura_controller(cultura_id)
    else: return 'Method is Not Allowed'