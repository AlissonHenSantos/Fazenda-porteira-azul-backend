# ...existing code...
from flask import request, jsonify, abort
import uuid

from .. import db
from .models import Funcionario

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

def list_all_funcionario_controller():
    funcionario = Funcionario.query.all()
    response = []
    for u in funcionario:
        response.append(u.toDict())
    return jsonify(response)

def create_funcionario_controller():
    data = _get_request_data()
    required = ['nome', 'idCultura']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': 'Missing fields', 'missing': missing}), 400

    id = str(uuid.uuid4())
    new_funcionario = Funcionario(
        id=id,
        nome=data['nome'],
        idCultura=data['idCultura'],
    )
    db.session.add(new_funcionario)
    db.session.commit()

    return jsonify(new_funcionario.toDict()), 201

def retrieve_funcionario_controller(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({'error': 'Funcionario not found'}), 404
    return jsonify(funcionario.toDict())

def update_funcionario_controller(funcionario_id):
    data = _get_request_data()
    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({'error': 'funcionario not found'}), 404

    # update only provided fields
    if 'nome' in data: funcionario.nome = data['nome']
    if 'idCultura' in data: funcionario.idCultura = data['idCultura']

    db.session.commit()

    return jsonify(funcionario.toDict())

def delete_funcionario_controller(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({'error': 'funcionario not found'}), 404
    db.session.delete(funcionario)
    db.session.commit()
    return '', 204
