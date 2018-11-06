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
    # HTTPS
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=('./security/test_cert.pem', './security/test_key.pem'))
