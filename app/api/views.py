from . import api
from flask.json import jsonify
from .models import Weather_Station, Forecast, User
import json


@api.route('/')
def index():
    return "it works"


@api.route('/users/<int:id>', methods=['GET'])
def get_users(id):
    user = User.query.filter_by(id=id).all()
    return jsonify(json.dumps(user))


@api.route('/test', methods=['GET'])
def test_response():
    return jsonify(test="it works!")
