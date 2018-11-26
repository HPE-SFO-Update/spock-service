import io
from library.util import Tools
from flask import send_file, jsonify
from flask import request, abort
from flask_restful import Resource
from library.security.Authorization import authorize


class UpdateInfoV1(Resource):
    """
    The class for Update Info version 1 uri
    """

    def post(self):
        """
        the request will send the following json -> {"version":<version number>,"sub_version":<sub_version number>}
        :return: json response
        """
        data = request.json
        sfo_version = data["sfo_version"]
        spock_version = data["spock_version"]
        return jsonify(Tools.check_update_file_map(sfo_version, spock_version))


class UpdateDownloadV1(Resource):
    """
    The class for Update Download version 1 uri
    """

    def get(self, file_name):
        """
        This allows to download the spock file
        :param file_name: spock file name
        :return: binary of spock file
        """
        version_stats = Tools.get_version_filename(file_name)
        path = Tools.get_file(version_stats.major_version, version_stats.minor_version, "./files/")
        if path is not None:
            with open(path, 'rb') as download_file:
                return send_file(
                    io.BytesIO(download_file.read()),
                    attachment_filename=file_name)
