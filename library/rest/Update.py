import io
from library.util import Tools
from flask import send_file, jsonify
from flask import request, abort
from flask_restful import Resource


class UpdateInfoV1(Resource):

    def post(self):
        data = request.json
        version = data["version"]
        sub_version = data["sub_version"]
        return jsonify(Tools.check_updated_file_exists(version, sub_version, "./files/"))


class UpdateDownloadV1(Resource):

    def get(self, file_name):
        version_stats = Tools.get_version_filename(file_name)
        path = Tools.get_file(version_stats.major_version, version_stats.minor_version, "./files/")
        if path is not None:
            with open(path, 'rb') as download_file:
                return send_file(
                    io.BytesIO(download_file.read()),
                    attachment_filename=file_name)
