#!/usr/bin/env python3
import os
import re
from flask import jsonify, make_response, abort
from library.util.SpockMap import SpockMap, parse_sfo_version


FILE_EXTENSION = ".zip"
REGEX_SFO_FILE = r"SFO_FILE_\d+_v_\d+\.zip"
_version = {"major_version": 0, "minor_version": 0, "filename": "SFO_FILE_0_v_0.zip"}


def get_file(version, subversion, root_dir):
    """
    Searches for file based on version and subversion number
    :param version: version (integer)
    :param subversion: sub_version (integer)
    :param root_dir: directory to search for spock file
    :return: path to spock file on local system
    """
    filtered_dir = list(filter(lambda x: re.match(REGEX_SFO_FILE, x) is not None, os.listdir(root_dir)))
    file_name = compile_file_name(version, subversion)
    if file_name in filtered_dir:
        return os.path.join(root_dir, file_name)
    else:
        return None


def compile_file_name(major_version, minor_version):
    """

    :param major_version:
    :param minor_version:
    :return:
    """
    return "SFO_FILE_{major_version}_v_{minor_version}{extension}".format(major_version=major_version,
                                                                          minor_version=minor_version,
                                                                          extension=FILE_EXTENSION)


def compile_spock_name(sfo_major_version, sfo_minor_version, sfo_build_version, spock_version):
    return "SPOCKUpdate{sfo_major_version}_{sfo_minor_version}_{sfo_build_version}_{spock_version}.zip".format(sfo_major_version=sfo_major_version,
                                                                                                               sfo_minor_version=sfo_minor_version,
                                                                                                               sfo_build_version=sfo_build_version,
                                                                                                               spock_version=spock_version)


def get_version_filename(filename):
    """
    Parses file name to figure out version
    :param filename: spock file name
    :return: version object
    """
    _filename = filename.replace("SFO_FILE_", "").replace(FILE_EXTENSION, "").split("_v_")
    return Version(int(_filename[0]), int(_filename[1]))


def api_version_prefix(api_version):
    """
    Adds api version to uri as a prefix
    :param api_version: api version
    :return: returns api version prefix
    """
    if api_version == 1:
        return '/v1'
    raise Exception("Invalid api version")


def check_updated_file_exists(current_major_version, current_minor_version, root_dir, api_version=1):
    """
    Checks if the file version in question needs to be updated
    :param current_major_version: major version (integer)
    :param current_minor_version: minor version (integer)
    :param root_dir: directory of the spock files are located
    :param api_version: api version (integer)
    :return: json response
    {
        "uri":<>,
        "need_to_update":<>,
        "filename":<>,
        "major_version":<>,
        "minor_version":<>
    }
    """
    _response = {"uri": "/update/download/", "need_to_update": True,
                 "major_version": "", "minor_version": "", "filename": ""}
    current_version = Version(current_major_version, current_minor_version)
    filtered_dir = list(filter(lambda x: re.match(REGEX_SFO_FILE, x) is not None, os.listdir(root_dir)))
    converted_dir = list(map(lambda x: get_version_filename(x), filtered_dir))
    updated_file = list(filter(lambda x: x > current_version, converted_dir))
    updated_file.sort(reverse=True)
    if len(updated_file) == 0:
        _response["uri"] = api_version_prefix(api_version)+ _response["uri"] + current_version.filename
        _response["need_to_update"] = False
        _response["filename"] = current_version.filename
        _response["major_version"] = current_version.major_version
        _response["minor_version"] = current_version.minor_version
        return _response
    else:
        _response["uri"] = api_version_prefix(api_version) + _response["uri"] + updated_file[0].filename
        _response["need_to_update"] = True
        _response["filename"] = updated_file[0].filename
        _response["major_version"] = updated_file[0].major_version
        _response["minor_version"] = updated_file[0].minor_version
        return _response


def check_update_file_map(sfo_version, spock_version):
    _response = {"uri": "", "need_to_update": True,
                 "sfo_version": "", "spock_version": ""}
    _map = SpockMap.get_instance()
    try:
        major, minor, build = parse_sfo_version(sfo_version)
        spock_list = _map.look_up_spocks(major_version=major, minor_version=minor, build_version=build)
        spock_item = SpockMap.get_latest_spock(spock_list)

        if spock_item is None:
            abort(make_response(jsonify({"message": "Smart Fabric Orchestrator Version is invalid"}), 400))

        if int(spock_version) >= int(spock_item[0]):
            _response["need_to_update"] = False

        _response["sfo_version"] = sfo_version
        _response["uri"] = spock_item[1]
        _response["spock_version"] = spock_item[0]
    except (TypeError, AttributeError, KeyError, ValueError):
        abort(make_response(jsonify({"message": "Invalid info given"}), 400))

    return _response


class Version(object):
    def __init__(self, major_version, minor_version):
        """ Major Version and Minor Version"""
        self.major_version = major_version
        self.minor_version = minor_version
        self.filename = compile_file_name(major_version, minor_version)

    def __gt__(self, object):
        return (self.major_version > object.major_version) or ((self.major_version == object.major_version) and (self.minor_version > object.minor_version))

    def __le__(self, object):
        return (self == object) or (self < object)

    def __ge__(self, object):
        return (self == object) or (self > object)

    def __eq__(self, object):
        return (self.major_version == object.major_version) and (self.major_version == object.major_version)

    def __ne__(self, object):
        return (self.major_version != object.major_version) or (self.major_version != object.major_version)

    def __lt__(self, object):
        return (self.major_version < object.major_version) or (
                    (self.major_version >= object.major_version) and (self.minor_version < object.minor_version))

    def __str__(self):
        return compile_file_name(self.major_version, self.minor_version)


def get_top_directory():
    special_dirs = ['library', 'files', 'security', 'config']
    current_directory = os.getcwd()
    for sp_dir in special_dirs:
        if sp_dir in current_directory:
            return current_directory.split(sp_dir)[0]
    return current_directory


def path_from_top_directory(path):
    return os.path.join(get_top_directory(), path)


if __name__ == "__main__":
    print(check_updated_file_exists(2, 0, "../../files"))