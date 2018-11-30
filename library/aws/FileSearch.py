# https://realpython.com/python-boto3-aws-s3/
import re
import boto3
from botocore.exceptions import ClientError
from library.util.MetaClasses import Singleton
from library.util.Tools import path_from_top_directory
from library.constants.Map import MAP_PATH


REGEX_SPOCK_FILE = r"SPOCKUpdate\d+_\d+_\d+_\d+\.zip"
REGEX_MAP_FILE = r"SFO-spock-ver-map.json"


class SpockRetrieve(metaclass=Singleton):
    __instance = None
    
    def __init__(self):
        if SpockRetrieve.__instance is None:
            SpockRetrieve.__instance = self
            self.s3_resource = boto3.resource('s3')
            self.object_files = {}
            self.map_modified = None
        else:
            raise Exception("Use SpockRetrieve.get_instance()")

    @staticmethod
    def get_instance():
        if SpockRetrieve.__instance is None:
            SpockRetrieve.__instance = SpockRetrieve()
            SpockRetrieve.__instance._download_map()
        return SpockRetrieve.__instance

    @staticmethod
    def initialize():
        return SpockRetrieve.get_instance()

    @staticmethod
    def download_map():
        SpockRetrieve.get_instance()._download_map()

    def update_object(self):
        _buckets = self.s3_resource.buckets.all()
        for bucket in _buckets:
            for obj in bucket.objects.all():
                if re.match(REGEX_SPOCK_FILE, obj.key):
                    self.object_files[obj.key] = obj

    def _update_map(self):
        _buckets = self.s3_resource.buckets.all()
        for bucket in _buckets:
            for obj in bucket.objects.all():
                if re.match(REGEX_MAP_FILE, obj.key):
                    return obj, obj.last_modified

    def _should_i_download_map(self):
        obj, date = self._update_map()
        if self.map_modified is None:
            self.map_modified = date
            return True, obj

        if self.map_modified < date:
            return True, obj
        else:
            return False, obj

    def _download_map(self):
        should_download, map_object = self._should_i_download_map()
        try:
            if should_download:
                _bucket = map_object.bucket_name
                self.s3_resource.Bucket(_bucket).download_file(map_object.key, path_from_top_directory(MAP_PATH))
                print("Downloaded map from bucket "+_bucket)
        except ClientError:
            print("Unable to download map")

    def find_spock_file_key(self, file_key):
        if file_key in self.object_files.keys():
            return self.object_files[file_key]
        return None


if __name__ == "__main__":
    SpockRetrieve.initialize()
    SpockRetrieve.download_map()


