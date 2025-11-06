# ...existing code...
from flask import request, jsonify, abort
import uuid
from datetime import datetime, date

from .. import db
from .models import UsoMaquinario

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

def list_all_usoMaquinario_controller():
    usoMaquinario = UsoMaquinario.query.all()
    response = []
    for u in usoMaquinario:
        response.append(u.toDict())
    return jsonify(response)

def create_usoMaquinario_controller():
    data = _get_request_data()
    required = ['idCultura', 'idMaquinario', 'tempo_uso']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': 'Missing fields', 'missing': missing}), 400

    try:
        tempo_uso = float(data['tempo_uso'])
    except (ValueError, TypeError):
        return jsonify({'error': 'tempo_uso deve ser um número'}), 400

    if 'data_uso' in data and data['data_uso']:
        dt_raw = data['data_uso']
        date_obj = None
        for fmt in ('%d-%m-%Y'):
            try:
                date_obj = datetime.strptime(dt_raw, fmt).date()
                break
            except (ValueError, TypeError):
                continue
        if date_obj is None:
            return jsonify({'error': 'Formato de data inválido. Use DD-MM-YYYY'}), 400
    else:
        date_obj = datetime.utcnow().date()

    id = str(uuid.uuid4())
    new_usoMaquinario = UsoMaquinario(
        id=id,
        idCultura=data['idCultura'],
        idMaquinario=data['idMaquinario'],
        tempo_uso=tempo_uso,
        data_uso=date_obj
    )
    db.session.add(new_usoMaquinario)
    db.session.commit()

    return jsonify(new_usoMaquinario.toDict()), 201

def retrieve_usoMaquinario_controller(usoMaquinario_id):
    usoMaquinario = UsoMaquinario.query.get(usoMaquinario_id)
    if not usoMaquinario:
        return jsonify({'error': 'Uso Maquinario not found'}), 404
    return jsonify(usoMaquinario.toDict())

def update_usoMaquinario_controller(usoMaquinario_id):
    data = _get_request_data()
    usoMaquinario = UsoMaquinario.query.get(usoMaquinario_id)
    if not usoMaquinario:
        return jsonify({'error': 'Uso Maquinario not found'}), 404

    if 'idCultura' in data: usoMaquinario.idCultura = data['idCultura']
    if 'idMaquinario' in data: usoMaquinario.idMaquinario = data['idMaquinario']
    if 'tempo_uso' in data: usoMaquinario.tempo_uso = float(data['tempo_uso'])

    db.session.commit()

    return jsonify(usoMaquinario.toDict())

def delete_usoMaquinario_controller(usoMaquinario_id):
    usoMaquinario = UsoMaquinario.query.get(usoMaquinario_id)
    if not usoMaquinario:
        return jsonify({'error': 'Uso Maquinario not found'}), 404
    db.session.delete(usoMaquinario)
    db.session.commit()
    return '', 204
