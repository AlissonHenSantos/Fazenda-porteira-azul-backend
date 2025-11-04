# ...existing code...
from flask import request, jsonify, abort
import uuid

from .. import db
from .models import CotacaoCultura

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

def list_all_cotacaoCultura_controller():
    cotacaoCultura = CotacaoCultura.query.all()
    response = []
    for u in cotacaoCultura:
        response.append(u.toDict())
    return jsonify(response)

def create_cotacaoCultura_controller():
    data = _get_request_data()
    required = ['value', 'idCultura']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': 'Missing fields', 'missing': missing}), 400

    id = str(uuid.uuid4())
    new_cotacaoCultura = CotacaoCultura(
        id=id,
        value=float(data['value']),
        idCultura=data['idCultura'],
    )
    db.session.add(new_cotacaoCultura)
    db.session.commit()

    return jsonify(new_cotacaoCultura.toDict()), 201

def retrieve_cotacaoCultura_controller(cotacaoCultura_id):
    cotacaoCultura = CotacaoCultura.query.get(cotacaoCultura_id)
    if not cotacaoCultura:
        return jsonify({'error': 'Cotação Cultura not found'}), 404
    return jsonify(cotacaoCultura.toDict())

def update_cotacaoCultura_controller(cotacaoCultura_id):
    data = _get_request_data()
    cotacaoCultura = CotacaoCultura.query.get(cotacaoCultura_id)
    if not cotacaoCultura:
        return jsonify({'error': 'Cotação Cultura not found'}), 404

    # update only provided fields
    if 'value' in data: cotacaoCultura.value = data['value']
    if 'idCultura' in data: cotacaoCultura.idCultura = data['idCultura']

    db.session.commit()

    return jsonify(cotacaoCultura.toDict())

def delete_cotacaoCultura_controller(cotacaoCultura_id):
    cotacaoCultura = CotacaoCultura.query.get(cotacaoCultura_id)
    if not cotacaoCultura:
        return jsonify({'error': 'Cotacao Cultura not found'}), 404
    db.session.delete(cotacaoCultura)
    db.session.commit()
    return '', 204
