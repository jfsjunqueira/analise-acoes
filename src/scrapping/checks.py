import os


def check_already_downloaded(file_path):
    return True if os.path.isfile(file_path) else False