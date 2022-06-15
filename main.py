from src.scrapping.extract import download_file, unzip_file
from src.config import *


def main():
    file_name = download_file(CVM_URL, dest_folder=DATA_PATH)
    unzip_file(file_name, dest_folder=file_name[:-4])


while __name__ == "__main__":
    main()
    break
