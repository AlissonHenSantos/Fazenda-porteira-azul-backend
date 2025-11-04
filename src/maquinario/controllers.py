# ...existing code...
from flask import request, jsonify, abort
import uuid

from .. import db
from .models import Maquina

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

def list_all_maquina_controller():
    maquina = Maquina.query.all()
    response = []
    for u in maquina:
        response.append(u.toDict())
    return jsonify(response)

def create_maquina_controller():
    data = _get_request_data()
    required = ['maquina']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': 'Missing fields', 'missing': missing}), 400

    id = str(uuid.uuid4())
    new_maquina = Maquina(
        id=id,
        maquina=data['maquina'],  
    )
    db.session.add(new_maquina)
    db.session.commit()

    return jsonify(new_maquina.toDict()), 201

def retrieve_maquina_controller(maquina_id):
    maquina = Maquina.query.get(maquina_id)
    if not maquina:
        return jsonify({'error': 'Maquina not found'}), 404
    return jsonify(maquina.toDict())

def update_maquina_controller(maquina_id):
    data = _get_request_data()
    maquina = Maquina.query.get(maquina_id)
    if not maquina:
        return jsonify({'error': 'Maquina not found'}), 404

    # update only provided fields
    if 'maquina' in data: maquina.maquina = data['maquina']

    db.session.commit()

    return jsonify(maquina.toDict())

def delete_maquina_controller(maquina_id):
    maquina = maquina.query.get(maquina_id)
    if not maquina:
        return jsonify({'error': 'maquina not found'}), 404
    db.session.delete(maquina)
    db.session.commit()
    return '', 204
