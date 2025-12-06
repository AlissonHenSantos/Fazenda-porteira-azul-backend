from flask import request, jsonify, abort
import uuid
from datetime import datetime

from .. import db
from .models import UsoMaquinario

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

def _parse_datetime(date_str):
    """Converte string ISO para datetime"""
    if not date_str:
        return None
    if isinstance(date_str, datetime):
        return date_str
    try:
        # Remove 'Z' e milissegundos se existirem
        date_str = date_str.replace('Z', '').split('.')[0]
        return datetime.fromisoformat(date_str)
    except:
        return None

def _get_related_name(obj, rel_attr_name, model_path, model_name, name_attr='nome', fk_field=None):
    try:
        rel = getattr(obj, rel_attr_name, None)
        if rel is not None:
            return getattr(rel, name_attr, getattr(rel, 'name', None)) or rel
    except Exception:
        pass

    try:
        module = __import__(model_path, fromlist=[model_name])
        Model = getattr(module, model_name)
        fk = None
        if fk_field and hasattr(obj, fk_field):
            fk = getattr(obj, fk_field)
        candidate = f"id{rel_attr_name.capitalize()}"
        if fk is None and hasattr(obj, candidate):
            fk = getattr(obj, candidate)
        if fk:
            related = Model.query.get(fk)
            if related:
                return getattr(related, name_attr, getattr(related, 'name', fk))
    except Exception:
        pass

    return fk if 'fk' in locals() else None

# --- list / create / retrieve / update / delete using the names expected by urls.py ---

def list_all_usoMaquinario_controller():
    usos = UsoMaquinario.query.all()
    response = []
    for u in usos:
        d = u.toDict()
        maquinario_name = _get_related_name(u, 'maquinario', 'src.maquinario.models', 'Maquinario', 'maquina', fk_field='idMaquinario')
        d['maquinario_nome'] = maquinario_name
        funcionario_name = _get_related_name(u, 'funcionario', 'src.funcionario.models', 'Funcionario', 'nome', fk_field='idFuncionario')
        d['funcionario_nome'] = funcionario_name
        response.append(d)
    return jsonify(response)

def create_usoMaquinario_controller():
    data = _get_request_data()
    required = ['idMaquinario', 'idFuncionario', 'data_inicio']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': 'Missing fields', 'missing': missing}), 400

    data_inicio = _parse_datetime(data['data_inicio'])
    data_fim = _parse_datetime(data.get('data_fim'))

    if not data_inicio:
        return jsonify({'error': 'data_inicio inválida'}), 400

    id = str(uuid.uuid4())
    new_uso = UsoMaquinario(
        id=id,
        idMaquinario=data['idMaquinario'],
        idFuncionario=data['idFuncionario'],
        data_inicio=data_inicio,
        data_fim=data_fim
    )
    db.session.add(new_uso)
    db.session.commit()

    d = new_uso.toDict()
    maquinario_name = _get_related_name(new_uso, 'maquinario', 'src.maquinario.models', 'Maquinario', 'maquina', fk_field='idMaquinario')
    d['maquinario_nome'] = maquinario_name
    funcionario_name = _get_related_name(new_uso, 'funcionario', 'src.funcionario.models', 'Funcionario', 'nome', fk_field='idFuncionario')
    d['funcionario_nome'] = funcionario_name

    return jsonify(d), 201

def retrieve_usoMaquinario_controller(uso_id):
    uso = UsoMaquinario.query.get(uso_id)
    if not uso:
        return jsonify({'error':'Uso not found'}), 404
    d = uso.toDict()
    maquinario_name = _get_related_name(uso, 'maquinario', 'src.maquinario.models', 'Maquinario', 'maquina', fk_field='idMaquinario')
    d['maquinario_nome'] = maquinario_name
    funcionario_name = _get_related_name(uso, 'funcionario', 'src.funcionario.models', 'Funcionario', 'nome', fk_field='idFuncionario')
    d['funcionario_nome'] = funcionario_name
    return jsonify(d)

def update_usoMaquinario_controller(uso_id):
    data = _get_request_data()
    uso = UsoMaquinario.query.get(uso_id)
    if not uso:
        return jsonify({'error':'Uso not found'}), 404

    if 'idMaquinario' in data:
        uso.idMaquinario = data['idMaquinario']
    if 'idFuncionario' in data:
        uso.idFuncionario = data['idFuncionario']
    if 'data_inicio' in data:
        data_inicio = _parse_datetime(data['data_inicio'])
        if data_inicio:
            uso.data_inicio = data_inicio
    if 'data_fim' in data:
        data_fim = _parse_datetime(data['data_fim'])
        uso.data_fim = data_fim

    db.session.commit()

    d = uso.toDict()
    maquinario_name = _get_related_name(uso, 'maquinario', 'src.maquinario.models', 'Maquinario', 'maquina', fk_field='idMaquinario')
    d['maquinario_nome'] = maquinario_name
    funcionario_name = _get_related_name(uso, 'funcionario', 'src.funcionario.models', 'Funcionario', 'nome', fk_field='idFuncionario')
    d['funcionario_nome'] = funcionario_name
    return jsonify(d)

def delete_usoMaquinario_controller(uso_id):
    uso = UsoMaquinario.query.get(uso_id)
    if not uso:
        return jsonify({'error':'Uso not found'}), 404
    db.session.delete(uso)
    db.session.commit()
    return '', 204

# Backwards-compatible aliases (optional)
list_all_uso_controller = list_all_usoMaquinario_controller
create_uso_controller = create_usoMaquinario_controller
retrieve_uso_controller = retrieve_usoMaquinario_controller
update_uso_controller = update_usoMaquinario_controller
delete_uso_controller = delete_usoMaquinario_controller