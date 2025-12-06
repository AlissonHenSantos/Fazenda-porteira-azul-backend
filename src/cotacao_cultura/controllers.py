# ...existing code...
from flask import request, jsonify, abort
import uuid

from .. import db
from .models import CotacaoCultura

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

def _get_cultura_name_from_instance(obj, idCultura):
    try:
        if hasattr(obj, 'cultura') and getattr(obj, 'cultura') is not None:
            cultura_obj = getattr(obj, 'cultura')
            return getattr(cultura_obj, 'nome', getattr(cultura_obj, 'name', None))
    except Exception:
        pass

    try:
        from ..cultura.models import Cultura
        c = Cultura.query.get(idCultura)
        if c:
            return getattr(c, 'nome', getattr(c, 'name', None))
    except Exception:
        pass

    return idCultura

def list_all_cotacaoCultura_controller():
    cotacaoCultura = CotacaoCultura.query.all()
    response = []
    for u in cotacaoCultura:
        d = u.toDict()
        idCultura = d.get('idCultura')
        cultura_name = _get_cultura_name_from_instance(u, idCultura)
        d.pop('idCultura', None)
        d['cultura'] = cultura_name
        response.append(d)
    return jsonify(response)

def create_cotacaoCultura_controller():
    data = _get_request_data()
    required = ['precoAtual', 'idCultura', 'precoAlvoVenda', 'variacao24h']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': 'Missing fields', 'missing': missing}), 400

    id = str(uuid.uuid4())
    new_cotacaoCultura = CotacaoCultura(
        id=id,
        precoAtual=float(data['precoAtual']),
        precoAlvoVenda=float(data['precoAlvoVenda']),
        variacao24h=float(data['variacao24h']),
        idCultura=data['idCultura'],
    )
    db.session.add(new_cotacaoCultura)
    db.session.commit()

    d = new_cotacaoCultura.toDict()
    cultura_name = _get_cultura_name_from_instance(new_cotacaoCultura, d.get('idCultura'))
    d.pop('idCultura', None)
    d['cultura'] = cultura_name

    return jsonify(d), 201

def retrieve_cotacaoCultura_controller(cotacaoCultura_id):
    cotacaoCultura = CotacaoCultura.query.get(cotacaoCultura_id)
    if not cotacaoCultura:
        return jsonify({'error': 'Cotação not found'}), 404
    d = cotacaoCultura.toDict()
    cultura_name = _get_cultura_name_from_instance(cotacaoCultura, d.get('idCultura'))
    d.pop('idCultura', None)
    d['cultura'] = cultura_name
    return jsonify(d)

def update_cotacaoCultura_controller(cotacaoCultura_id):
    data = _get_request_data()
    cotacaoCultura = CotacaoCultura.query.get(cotacaoCultura_id)
    if not cotacaoCultura:
        return jsonify({'error': 'Cotação not found'}), 404

    if 'precoAtual' in data: cotacaoCultura.precoAtual = float(data['precoAtual'])
    if 'precoAlvoVenda' in data: cotacaoCultura.precoAlvoVenda = float(data['precoAlvoVenda'])
    if 'variacao24h' in data: cotacaoCultura.variacao24h = float(data['variacao24h'])
    if 'idCultura' in data: cotacaoCultura.idCultura = data['idCultura']

    db.session.commit()

    d = cotacaoCultura.toDict()
    cultura_name = _get_cultura_name_from_instance(cotacaoCultura, d.get('idCultura'))
    d.pop('idCultura', None)
    d['cultura'] = cultura_name

    return jsonify(d)

def delete_cotacaoCultura_controller(cotacaoCultura_id):
    cotacaoCultura = CotacaoCultura.query.get(cotacaoCultura_id)
    if not cotacaoCultura:
        return jsonify({'error': 'Cotação not found'}), 404
    db.session.delete(cotacaoCultura)
    db.session.commit()
    return '', 204
# ...existing code...