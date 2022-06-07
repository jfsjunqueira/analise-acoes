import os
from scrapping_config import DATA_PATH


def check_already_downloaded(file_path):
    return True if os.path.isfile(file_path) else False