# ...existing code...
from flask import request, jsonify, abort
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid

from .. import db
from .models import User

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

def list_all_users_controller():
    users = User.query.all()
    response = []
    for u in users:
        response.append(u.toDict())
    return jsonify(response)

def create_user_controller():
    data = _get_request_data()
    required = ['email', 'username', 'password']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': 'Missing fields', 'missing': missing}), 400

    id = str(uuid.uuid4())
    new_user = User(
        id=id,
        email=data['email'],
        username=data['username'],
        password=generate_password_hash(data['password']).decode('utf-8')
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.toDict()), 201

def retrieve_user_controller(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.toDict())

def update_user_controller(user_id):
    data = _get_request_data()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # update only provided fields
    if 'email' in data: user.email = data['email']
    if 'username' in data: user.username = data['username']
    if 'password' in data: user.password = data['password']

    db.session.commit()

    return jsonify(user.toDict())

def delete_user_controller(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return '', 204
# ...existing code...

def login_controller():
    data = _get_request_data()
    required = ['email', 'password']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': 'Missing fields', 'missing': missing}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200