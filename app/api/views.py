from . import api
from flask import g
from flask.json import jsonify
from .models import User
from .errors import ErrorResponse
from flask.ext.httpauth import HTTPBasicAuth
import json


authorization_check = HTTPBasicAuth()


@authorization_check.verify_password
def verify_password(name_or_token, password):
    if name_or_token == '':
        g.current_user = None
        g.token_used = False
        return False
    if password == '':
        g.current_user = User.verify_auth_token(name_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(name=name_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@api.route('/token')
@authorization_check.login_required
def get_token():
    if (g.current_user is None) or g.token_used:
        return ErrorResponse.unauthorized('Invalid credentials')
    return jsonify(
            {'token': g.current_user.generate_auth_token().decode('utf-8'),
             'expiration': 600})


@authorization_check.error_handler
def auth_error():
    return ErrorResponse.forbidden('Unconfirmed user')


@api.route('/secret')
@authorization_check.login_required
def get_secret():
    return jsonify(message='Secret message!')


@api.route('/users/<int:id>', methods=['GET'])
def get_users(id):
    user = User.query.filter_by(id=id).all()
    return jsonify(message='In progress...')


@api.route('/test', methods=['GET'])
def test_response():
    return jsonify(test="it works!")
