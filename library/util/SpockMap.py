import json


'''
    map.json
    {"major_version":{"minor_version":{"build_version":[{"spock_version":"url"}]}}
    
    Example:
    {"1":{"1":{"0":[{"420":"url"}]}}
'''
class SpockMap(object):

    def __init__(self):
        self.data = {}

    def open(self, filepath):
        with open(filepath, 'r') as file:
            self.data = json.load(file)

    def write(self, filepath):
        with open(filepath, 'w') as file:
            file.write(json.dump(self.data))

    def look_up_spocks(self, major_version, minor_version, build_version="0"):
        spock_list = []
        try:
            spock_list = self.data[major_version][minor_version][build_version]
        except KeyError:
            pass
        return spock_list

    @staticmethod
    def get_latest_spocks(spock_list):
        try:
            sorted_spock_list = sorted(spock_list, key=lambda spock: spock.keys()[0])
            lastest = sorted_spock_list[0]
        except IndexError:
            latest = None
        return latest

    def add_spock_entry(self, major_version, minor_version, spock_version, spock_url,build_version="0"):
        pass