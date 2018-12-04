import os

def get_top_directory():
    special_dirs = ['library', 'files', 'security', 'config']
    current_directory = os.getcwd()
    for sp_dir in special_dirs:
        if sp_dir in current_directory:
            return current_directory.split(sp_dir)[0]
    return current_directory


def path_from_top_directory(path):
    return os.path.join(get_top_directory(), path)