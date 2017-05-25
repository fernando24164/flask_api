from . import api
from flask import g
from flask.json import jsonify
from .models import User, Weather_Station
from .errors import ErrorResponse
from flask_httpauth import HTTPBasicAuth


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


@api.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return jsonify(user.to_json())


@api.route('/station/<int:id>', methods=['GET'])
def get_station(id):
    station = Weather_Station.query.filter_by(id=id).first()
    return jsonify(station.to_json())


@api.route('/stations', methods=['GET'])
def get_stations():
    arr_response = []
    stations = Weather_Station.query.all()
    for station in stations:
        arr_response.append(station.to_json())
    return jsonify(arr_response)


@api.route('/test', methods=['GET'])
def test_response():
    return jsonify(test="it works!")
