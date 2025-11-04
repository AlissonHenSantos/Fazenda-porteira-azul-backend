# ...existing code...
from flask import request, jsonify, abort
import uuid
from datetime import datetime, timedelta

from .. import db
from .models import HorasFuncionario

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

def _check_weekly_hours(funcionario_id, new_hours):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    weekly_hours = HorasFuncionario.query.filter(
        HorasFuncionario.idFuncionario == funcionario_id,
        HorasFuncionario.data >= start_of_week,
        HorasFuncionario.data <= end_of_week
    ).with_entities(HorasFuncionario.horas).all()
    
    total_hours = sum(h[0] for h in weekly_hours)
    
    if total_hours + new_hours > 44:
        return False, total_hours
    return True, total_hours

def list_all_horasFuncionario_controller():
    horasFuncionario = HorasFuncionario.query.all()
    response = []
    for u in horasFuncionario:
        response.append(u.toDict())
    return jsonify(response)

def create_horasFuncionario_controller():
    data = _get_request_data()
    required = ['horas', 'idFuncionario']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': 'Missing fields', 'missing': missing}), 400

    try:
        horas = int(data['horas'])
    except ValueError:
        return jsonify({'error': 'Horas deve ser um número inteiro'}), 400

    allowed, total_hours = _check_weekly_hours(data['idFuncionario'], horas)
    if not allowed:
        return jsonify({
            'error': 'Limite semanal excedido para este funcionário',
            'horas_registradas': total_hours,
            'horas_restantes': 44 - total_hours,
            'idFuncionario': data['idFuncionario']
        }), 400

    id = str(uuid.uuid4())
    new_horasFuncionario = HorasFuncionario(
        id=id,
        horas=horas,
        idFuncionario=data['idFuncionario'],
    )
    db.session.add(new_horasFuncionario)
    db.session.commit()

    return jsonify(new_horasFuncionario.toDict()), 201

def retrieve_horasFuncionario_controller(horasFuncionario_id):
    horasFuncionario = HorasFuncionario.query.get(horasFuncionario_id)
    if not horasFuncionario:
        return jsonify({'error': 'Horas Funcionario not found'}), 404
    return jsonify(horasFuncionario.toDict())

def update_horasFuncionario_controller(horasFuncionario_id):
    data = _get_request_data()
    horasFuncionario = HorasFuncionario.query.get(horasFuncionario_id)
    if not horasFuncionario:
        return jsonify({'error': 'Hora funcionario not found'}), 404

    if 'horas' in data:
        try:
            new_hours = int(data['horas'])
            allowed, total_hours = _check_weekly_hours(
                horasFuncionario.idFuncionario,
                new_hours - horasFuncionario.horas 
            )
            if not allowed:
                return jsonify({
                    'error': 'Limite semanal excedido para este funcionário',
                    'horas_registradas': total_hours,
                    'horas_restantes': 44 - total_hours,
                    'idFuncionario': horasFuncionario.idFuncionario
                }), 400
            horasFuncionario.horas = new_hours
        except ValueError:
            return jsonify({'error': 'Horas deve ser um número inteiro'}), 400

    if 'idFuncionario' in data:
        horasFuncionario.idFuncionario = data['idFuncionario']

    db.session.commit()
    return jsonify(horasFuncionario.toDict())

def delete_horasFuncionario_controller(funcionario_id):
    horasFuncionario = HorasFuncionario.query.get(funcionario_id)
    if not horasFuncionario:
        return jsonify({'error': 'Horas Funcionario not found'}), 404
    db.session.delete(horasFuncionario)
    db.session.commit()
    return '', 204
