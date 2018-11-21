#!/usr/bin/env python3
import argparse
from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO
# from flask_login import LoginManager

from library.rest.Heartbeat import HeartbeatV1
from library.rest.Update import UpdateInfoV1, UpdateDownloadV1
from library.aws.FileSearch import SpockRetrieve
# from library.rest.LoginRest import LoginRestV1
# from library.socket.LoginSocket import Login

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# LoginManager(app)
api = Api(app)
api.add_resource(HeartbeatV1, '/v1/heartbeat')
api.add_resource(UpdateInfoV1, '/v1/update/info')
api.add_resource(UpdateDownloadV1, '/v1/update/download/<file_name>')
# api.add_resource(LoginRestV1, '/v1/rest/login')
socket = SocketIO(app)
# socket.on_namespace(Login('/v1/login'))


if __name__ == '__main__':
    # https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
    parser = argparse.ArgumentParser(description="Runs SFO Spock Update Service")
    parser.add_argument("--host", required=False, help="Hostname or IP address")
    parser.add_argument("-c", "--cert", required=False, help="The full path to public ssl certificate")
    parser.add_argument("-k", "--key", required=False, help="The full path to private ssl certificate")
    parser.add_argument("-p", "--port", type=int, required=True, help="The port in which the service will be exposed")
    parser.add_argument("-d", "--debug", required=False, action="store_true", help="The service will be in debug mode")
    args = parser.parse_args()

    if args.host is None:
        _host = '0.0.0.0'
    else:
        _host = args.host

    _port = args.port
    _debug = args.debug

    # SpockRetrieve.intialize()

    if args.cert is None and args.key is None:
        # HTTP
        socket.run(app, host=_host, port=_port, debug=_debug)
    else:
        # HTTPS
        _private_key = args.key  # ./security/test_key.pem
        _public_key = args.cert  # ./security/test_cert.pem
        socket.run(app, host=_host, port=_port, debug=_debug, ssl_context=(_public_key, _private_key))

