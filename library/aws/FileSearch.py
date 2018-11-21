# https://realpython.com/python-boto3-aws-s3/
import re
import boto3
from library.util.MetaClasses import Singleton

REGEX_SPOCK_FILE = r"SPOCKUpdate\d+_\d+_\d+_\d+\.zip"


class SpockRetrieve(metaclass=Singleton):
    __instance = None

    def __init__(self):
        if SpockRetrieve.__instance is None:
            SpockRetrieve.__instance = self
            self.s3_resource = boto3.resource('s3')
            self.object_files = {}
        else:
            raise Exception("Use SpockRetrieve.get_instance()")

    @staticmethod
    def get_instance():
        if SpockRetrieve.__instance is None:
            SpockRetrieve.__instance = SpockRetrieve()
            SpockRetrieve.__instance.update_object()
        return SpockRetrieve.__instance

    def update_object(self):
        _buckets = self.s3_resource.buckets.all()
        for bucket in _buckets:
            for obj in bucket.objects.all():
                if re.match(REGEX_SPOCK_FILE, obj.key):
                    self.object_files[obj.key] = obj

    def find_spock_file_key(self, file_key):
        if file_key in self.object_files.keys():
            return self.object_files[file_key]
        return None


if __name__ == "__main__":
    resource = SpockRetrieve.get_instance()
    print(resource.find_spock_file_key('SPOCKUpdate1_1_0_220.zip').key)
