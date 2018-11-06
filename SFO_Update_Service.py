#!/usr/bin/env python3
import io
import os
import argparse
from flask import Flask, send_file, jsonify
from flask import request, abort
from library.util import Tools

app = Flask(__name__)


@app.route("/")
def main_root():
    return "Smart Fabric Orchestrator Update Service"


@app.route("/v1/heartbeat", methods=['GET'])
def heartbeat():
    return "Smart Fabric Orchestrator Update Service"


@app.route('/v1/update/info', methods=['POST'])
def determine_update():
    if request.method == 'POST':
        data = request.json
        version = data["version"]
        sub_version = data["sub_version"]
        return jsonify(Tools.check_updated_file_exists(version, sub_version, "./files/"))

    abort(400, "Bad Request")


# https://gist.github.com/Miserlou/fcf0e9410364d98a853cb7ff42efd35a
@app.route("/v1/update/download/<file_name>", methods=['GET'])
def download_update(file_name):
    if request.method == 'GET':
        version_stats = Tools.get_version_filename(file_name)
        path = Tools.get_file(version_stats.major_version, version_stats.minor_version, "./files/")
        if path is not None:
            with open(path, 'rb') as download_file:
                return send_file(
                    io.BytesIO(download_file.read()),
                    attachment_filename=file_name)

    abort(400, "Bad Request")


# https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
if __name__ == '__main__':
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

    if args.cert is not None and args.key is not None:
        # HTTPS
        _private_key = args.key  # ./security/test_key.pem
        _public_key = args.cert  # ./security/test_cert.pem
        app.run(host=_host, port=_port, debug=_debug, ssl_context=(_public_key, _private_key))
    else:
        # HTTP
        app.run(host=_host, port=_port, debug=_debug)
