from flask import jsonify


class ErrorResponse():

    def unauthorized(message):
        response = jsonify({'error': 'unauthorized', 'message': message})
        response.status_code = 401
        return response

    def forbidden(message):
        response = jsonify({'error': 'forbidden', 'message': message})
        response.status_code = 403
        return response
