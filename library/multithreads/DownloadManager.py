import os
import sys
import boto3, botocore.errorfactory
from library.util.MetaClasses import Singleton
from library.util.Path import get_top_directory
from library.util.Path import path_from_top_directory


class DownloadManager(object, metaclass=Singleton):
    __instance = None

    def __init__(self):
        if DownloadManager.__instance is None:
            DownloadManager.__instance = self
            self.s3_resource = boto3.resource('s3')
            self.download_dir = None

        else:
            raise Exception("Use DownloadManager.get_instance()")

    @staticmethod
    def get_instance():
        if DownloadManager.__instance is None:
            DownloadManager.__instance = DownloadManager()

        return DownloadManager.__instance

    @staticmethod
    def set_download_dir(download_dir):
        DownloadManager.get_instance().download_dir = download_dir
        DownloadManager.get_instance()._build_dir()

    def _build_dir(self):
        if self.download_dir is not None:
            if os.path.exists(path_from_top_directory(self.download_dir)) is False:
                os.makedirs(path_from_top_directory(self.download_dir))

    def download(self, file_name):
        if os.path.exists(os.path.join(path_from_top_directory(self.download_dir), file_name)):
            return True, os.path.join(path_from_top_directory(self.download_dir), file_name)

        exists, obj = self.search_file(file_name)

        if exists:
            _download_file = os.path.join(path_from_top_directory(self.download_dir), file_name)
            self.s3_resource.Bucket(obj.bucket_name).download_file(obj.key, _download_file)
            return True, _download_file

        return False, ""

    def search_file(self, file_name):
        _buckets = self.s3_resource.buckets.all()

        for bucket in _buckets:
            try:
                for obj in bucket.objects.all():
                    if file_name == obj.key:
                        return True, obj
            except botocore.errorfactory.ClientError:
                return False, None

        return False, None

    def get_file_from_downloads(self, file_name):
        _path = os.path.join(path_from_top_directory(self.download_dir), file_name)
        if os.path.exists(_path):
            return True, _path

        return False, ""


if __name__ == "__main__":
    path = os.path.join(get_top_directory(), "download", "SFO-spock-ver-map.json")
    print(path)
