# ...existing code...
from flask import request, jsonify, abort
import uuid

from .. import db
from .models import Cultura

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

def list_all_cultura_controller():
    cultura = Cultura.query.all()
    response = []
    for u in cultura:
        response.append(u.toDict())
    return jsonify(response)

def create_cultura_controller():
    data = _get_request_data()
    required = ['nome']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': 'Missing fields', 'missing': missing}), 400

    id = str(uuid.uuid4())
    new_cultura = Cultura(
        id=id,
        nome=data['nome'],
    )
    db.session.add(new_cultura)
    db.session.commit()

    return jsonify(new_cultura.toDict()), 201

def retrieve_cultura_controller(cultura_id):
    cultura = Cultura.query.get(cultura_id)
    if not cultura:
        return jsonify({'error': 'Cultura not found'}), 404
    return jsonify(cultura.toDict())

def update_cultura_controller(cultura_id):
    data = _get_request_data()
    cultura = Cultura.query.get(cultura_id)
    if not cultura:
        return jsonify({'error': 'Cultura not found'}), 404

    # update only provided fields
    if 'nome' in data: cultura.nome = data['nome']

    db.session.commit()

    return jsonify(cultura.toDict())

def delete_cultura_controller(cultura_id):
    cultura = Cultura.query.get(cultura_id)
    if not cultura:
        return jsonify({'error': 'Cultura not found'}), 404
    db.session.delete(cultura)
    db.session.commit()
    return '', 204
