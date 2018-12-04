import io
from library.util import Tools
from flask import send_file, jsonify
from flask import request, jsonify, make_response, abort
from flask_restful import Resource
from library.multithreads.Scheduler import check_spock_map
from library.multithreads.DownloadManager import DownloadManager


class UpdateInfoV1(Resource):
    """
    The class for Update Info version 1 uri
    """
    @check_spock_map
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
        exist, path = DownloadManager.get_instance().get_file_from_downloads(file_name)
        if exist is False:
            exist, path = DownloadManager.get_instance().download(file_name)

        if exist:
            with open(path, 'rb') as download_file:
                return send_file(
                    io.BytesIO(download_file.read()),
                    attachment_filename=file_name)
        abort(make_response(jsonify({"message": "{} file is not available for download or does not exist.".format(file_name)}), 400))
