from flask import request, jsonify
import uuid

from .. import db
from .models import user

def list_all_users_controller():
    users = user.query.all()
    response = []
    for user in users: response.append(user.toDict())
    return jsonify(response)

def create_user_controller():
    request_form = request.form.to_dict()

    id = str(uuid.uuid4())
    new_user = user(
                          id             = id,
                          email          = request_form['email'],
                          username       = request_form['username'],
                          password       = request_form['password']
                         
                          )
    db.session.add(new_user)
    db.session.commit()

    response = user.query.get(id).toDict()
    return jsonify(response)

def retrieve_user_controller(user_id):
    response = user.query.get(user_id).toDict()
    return jsonify(response)

def update_user_controller(user_id):
    request_form = request.form.to_dict()
    user = user.query.get(user_id)

    user.email        = request_form['email']
    user.username     = request_form['username']
    user.password     = request_form['password']
    
    db.session.commit()

    response = user.query.get(user_id).toDict()
    return jsonify(response)

def delete_user_controller(user_id):
    user.query.filter_by(id=user_id).delete()
    db.session.commit()
