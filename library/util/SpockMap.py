import json
from library.util.MetaClasses import Singleton


#
# SFO-spock-ver-map.json
# {"major_version":{"minor_version":{"build_version":[{"spock_version":"url"}]}}
#
# Example:
# {"1":{"1":{"0":[{"420":"url"}]}}
class SpockMap(object, metaclass=Singleton):
    __instance = None

    def __init__(self):
        if SpockMap.__instance is None:
            SpockMap.__instance = self
            self.data = {}
            self.file_path = None
        else:
            raise Exception("Use SpockMap.get_instance()")

    @staticmethod
    def get_instance():
        if SpockMap.__instance is None:
            SpockMap.__instance = SpockMap()

        return SpockMap.__instance

    @staticmethod
    def open(file_path):
        SpockMap.get_instance()._open(file_path)

    def _open(self, file_path):
        self.file_path = file_path
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except json.JSONDecodeError:
            self.write(self.file_path)

    def write(self, file_path):
        self.file_path = file_path
        with open(file_path, 'w') as file:
            json.dump(self.data, fp=file)

    def update(self):
        self.open(self.file_path)

    def look_up_spocks(self, major_version, minor_version, build_version="0"):
        spock_list = []
        try:
            _spock_list = self.data[major_version][minor_version][build_version]
            for dictionary in _spock_list:
                spock_list.extend([(k, v) for k, v in dictionary.items()])
        except KeyError:
            pass
        return spock_list

    @staticmethod
    def get_latest_spock(spock_list):
        try:
            sorted_spock_list = sorted(spock_list, key=lambda x: int(x[0]), reverse=True)
            latest = sorted_spock_list[0]
        except IndexError:
            latest = None
        return latest

    def add_spock_entry(self, major_version, minor_version, spock_version, spock_url, build_version="0"):
        spock_entry = {spock_version: spock_url}
        if major_version in self.data:
            if minor_version in self.data[major_version]:
                if build_version in self.data[major_version][minor_version]:
                    spock_list = self.data[major_version][minor_version][build_version]
                    self.data[major_version][minor_version][build_version] = [x for x in spock_list if spock_version not in x]
                    self.data[major_version][minor_version][build_version].append(spock_entry)
                    return
                self.data[major_version][minor_version][build_version] = [spock_entry]
                return
            self.data[major_version].update({minor_version: {build_version: [spock_entry]}})
            return
        self.data.update({major_version: {minor_version: {build_version: [spock_entry]}}})


def parse_sfo_version(version):
    major, minor, build = version.split('.')
    return major, minor, build


if __name__ == "__main__":
    _map = SpockMap()
    _map.add_spock_entry(major_version="1", minor_version="1", build_version="0", spock_version="420",
                        spock_url="/spock-version.zip")
    print(_map.data)
    _map.add_spock_entry(major_version="1", minor_version="1", build_version="0", spock_version="423",
                        spock_url="/sp0ck-versi0n.zip")
    print(_map.data)
    _map.add_spock_entry(major_version="1", minor_version="1", build_version="0", spock_version="423",
                        spock_url="/spock-version.zip")
    print(_map.data)
    _map.add_spock_entry(major_version="1", minor_version="2", build_version="0", spock_version="423",
                        spock_url="/spock-version.zip")
    print(_map.data)
    _map.add_spock_entry(major_version="1", minor_version="2", build_version="32", spock_version="423",
                        spock_url="/spock-version.zip")
    print(_map.data)
    print(SpockMap.get_latest_spock(_map.look_up_spocks("1", "1", "0")))
