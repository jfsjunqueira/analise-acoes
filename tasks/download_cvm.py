""" Setting actual wd for task """

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


""" Actual task """

from src.scrapping.cvm import download_unzip
from src.base_logger import logger
from src.config import CVM_URL, DATA_PATH
from datetime import datetime
from tqdm import tqdm

CURRENT_YEAR = datetime.now().year

def main():
    url_list = [f'{CVM_URL[:-8]}{i}.zip' for i in range(2011,CURRENT_YEAR-1,1)]

    for url in tqdm(url_list, 'Downloading DFPs'):
        download_unzip(url, '../'+DATA_PATH)


while __name__ == "__main__": 
    logger.info(f"Starting to download DFPs for dates between and including 2011 and {CURRENT_YEAR - 1}")
    main()
    logger.info(f"CVM data succesfully downloaded!")
    logger.info(f"You can find everything inside the 'data' folder, on this project root directory.")
    break
