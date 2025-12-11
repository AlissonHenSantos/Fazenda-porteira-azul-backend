from flask import request, jsonify
import uuid
from datetime import datetime
from .. import db
from .models import CotacaoCultura
from ..cultura.models import Cultura

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

def list_all_cotacoes_controller():
    try:
        cotacoes = CotacaoCultura.query.order_by(CotacaoCultura.dataAtualizacao.desc()).all()
        return jsonify([c.toDict() for c in cotacoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_cotacao_controller():
    data = _get_request_data()
    
    required = ['idCultura', 'precoAtual']
    missing = [k for k in required if k not in data or data[k] == '']
    if missing:
        return jsonify({'error': 'Missing required fields', 'missing': missing}), 400
    
    try:
        cultura = Cultura.query.get(data['idCultura'])
        if not cultura:
            return jsonify({'error': 'Cultura not found'}), 404
        
        id = str(uuid.uuid4())
        nova_cotacao = CotacaoCultura(
            id=id,
            idCultura=data['idCultura'],
            precoAtual=float(data['precoAtual']),
            precoAlta=float(data['precoAlta']) if data.get('precoAlta') else None,
            precoBaixa=float(data['precoBaixa']) if data.get('precoBaixa') else None
        )
        
        db.session.add(nova_cotacao)
        db.session.commit()
        
        return jsonify(nova_cotacao.toDict()), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Invalid data type: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def retrieve_cotacao_controller(cotacao_id):
    try:
        cotacao = CotacaoCultura.query.get(cotacao_id)
        if not cotacao:
            return jsonify({'error': 'Cotação not found'}), 404
        return jsonify(cotacao.toDict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_cotacao_controller(cotacao_id):
    data = _get_request_data()
    
    try:
        cotacao = CotacaoCultura.query.get(cotacao_id)
        if not cotacao:
            return jsonify({'error': 'Cotação not found'}), 404
        
        if 'precoAtual' in data and data['precoAtual'] != '':
            cotacao.precoAtual = float(data['precoAtual'])
        
        if 'precoAlta' in data and data['precoAlta'] != '':
            cotacao.precoAlta = float(data['precoAlta'])
        
        if 'precoBaixa' in data and data['precoBaixa'] != '':
            cotacao.precoBaixa = float(data['precoBaixa'])
        
        db.session.commit()
        return jsonify(cotacao.toDict()), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Invalid data type: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def delete_cotacao_controller(cotacao_id):
    try:
        cotacao = CotacaoCultura.query.get(cotacao_id)
        if not cotacao:
            return jsonify({'error': 'Cotação not found'}), 404
        
        db.session.delete(cotacao)
        db.session.commit()
        
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_cotacao_by_cultura_controller(cultura_id):
    try:
        cotacoes = CotacaoCultura.query.filter_by(idCultura=cultura_id).order_by(
            CotacaoCultura.dataAtualizacao.desc()
        ).all()
        
        return jsonify([c.toDict() for c in cotacoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_cotacao_atual_controller(cultura_id):
    try:
        cotacao = CotacaoCultura.query.filter_by(idCultura=cultura_id).order_by(
            CotacaoCultura.dataAtualizacao.desc()
        ).first()
        
        if not cotacao:
            return jsonify({'error': 'No cotation data found for this culture'}), 404
        
        return jsonify(cotacao.toDict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500