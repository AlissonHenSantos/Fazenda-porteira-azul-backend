# ...existing code...
from flask import request, jsonify, abort
import uuid

from .. import db
from .models import Funcionario

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

def _get_cultura_name_from_instance(obj, idCultura):
    # tenta relacionamento first, depois tenta consultar o modelo Cultura
    try:
        if hasattr(obj, 'cultura') and getattr(obj, 'cultura') is not None:
            cultura_obj = getattr(obj, 'cultura')
            return getattr(cultura_obj, 'nome', getattr(cultura_obj, 'name', None))
    except Exception:
        pass

    # fallback: tentar importar e buscar pela FK
    try:
        from ..cultura.models import Cultura
        c = Cultura.query.get(idCultura)
        if c:
            return getattr(c, 'nome', getattr(c, 'name', None))
    except Exception:
        pass

    # último recurso: retorna o id
    return idCultura

def list_all_funcionario_controller():
    funcionario = Funcionario.query.all()
    response = []
    for u in funcionario:
        d = u.toDict()
        idCultura = d.get('idCultura')
        cultura_name = _get_cultura_name_from_instance(u, idCultura)
        # remover idCultura e adicionar campo 'cultura' com o nome
        d.pop('idCultura', None)
        d['cultura'] = cultura_name
        response.append(d)
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

    d = new_funcionario.toDict()
    cultura_name = _get_cultura_name_from_instance(new_funcionario, d.get('idCultura'))
    d.pop('idCultura', None)
    d['cultura'] = cultura_name

    return jsonify(d), 201

def retrieve_funcionario_controller(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({'error': 'Funcionario not found'}), 404
    d = funcionario.toDict()
    cultura_name = _get_cultura_name_from_instance(funcionario, d.get('idCultura'))
    d.pop('idCultura', None)
    d['cultura'] = cultura_name
    return jsonify(d)

def update_funcionario_controller(funcionario_id):
    data = _get_request_data()
    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({'error': 'funcionario not found'}), 404

    # update only provided fields
    if 'nome' in data: funcionario.nome = data['nome']
    if 'idCultura' in data: funcionario.idCultura = data['idCultura']

    db.session.commit()

    d = funcionario.toDict()
    cultura_name = _get_cultura_name_from_instance(funcionario, d.get('idCultura'))
    d.pop('idCultura', None)
    d['cultura'] = cultura_name

    return jsonify(d)

def delete_funcionario_controller(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({'error': 'funcionario not found'}), 404
    db.session.delete(funcionario)
    db.session.commit()
    return '', 204
# ...existing code...