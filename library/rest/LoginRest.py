from flask import request, abort, jsonify
from flask_restful import Resource
from library.security.TokenHandler import create_token


class LoginRestV1(Resource):
    """
    The class for login version 1 uri
    """
    def post(self):
        """
        Validated username and password and returns a token
        :return: json -> {'token':'<Json Web Token>'}
        """
        data = request.json
        # This is temporary code will be replaced by WebSocket Authentication - Arjun Kiran
        if data["username"] != 'admin':
            abort(400, {'message': 'Invalid Username'})

        if data["password"] != 'password':
            abort(400, {'message': 'Invalid Password'})
        token = create_token()
        return jsonify({'token': token})
