from flask import request, abort, jsonify
from flask_restful import Resource
from library.security.TokenHandler import create_token


class LoginRestV1(Resource):

    def post(self):
        data = request.json
        if data["username"] != 'admin':
            abort(400, {'message': 'Invalid Username'})

        if data["password"] != 'password':
            abort(400, {'message': 'Invalid Password'})
        token = create_token()
        return jsonify({'token': token})
