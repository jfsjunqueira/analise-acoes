import os
import zipfile

import requests
from pathlib import Path
from src.base_logger import logger
from src.scrapping.checks import check_already_downloaded


def download_unzip(url: str, dest_folder: Path) -> None:
    """Downloads and unzips file from target usrl to destination folder.

    Args:
        url (str): URL of the target file to be downloaded.
        dest_folder (pathlib.Path): Path to destination folder where file should be unziped.
    """
    logger.info("Downloading the file...")
    file_name = Path(download_file(url, dest_folder))
    logger.info("Unzipping the file...")
    unzip_file(file_name, dest_folder=file_name.parents[0].joinpath(file_name.stem))
    logger.info(f"File {file_name} successfuly downloaded to {dest_folder}!")


def create_if_not_dir(dest_folder: Path) -> None:
    """Creates a directory in dest_folder PATH if it doesn't exist yet.

    Args:
        dest_folder (pathlib.Path): Path to destination folder.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)


def download_file(url: str, dest_folder: Path) -> str:
    """Downloads file from a specified URL to a specified destination folder.

    Args:
        url (str): URL with the file to be downloaded.
        dest_folder (pathlib.Path): Path of the destination folder.

    Returns:
        str: File path of the downloaded file.
    """
    create_if_not_dir(dest_folder)

    filename = url.split("/")[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)
    if check_already_downloaded(file_path):
        logger.error(f"File {os.path.abspath(file_path)} already exists.")
        return file_path
    r = requests.get(url, stream=True)

    if r.ok:
        logger.info(f"Saving to {os.path.abspath(file_path)}")
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        logger.error(f"Download failed status code {r.status_code}\n{r.text}")
    return file_path


def unzip_file(file_path: Path, dest_folder: Path):
    """Unzips a .zip file to a specified destination folder.

    Args:
        file_path (str): Path of the .zip file.
        dest_folder (pathlib.Path): Destination folder where the unziped files should be stored.
    """
    if dest_folder.exists():
        logger.error(f"Folder {os.path.abspath(dest_folder)} already exists.")
    else:
        create_if_not_dir(dest_folder)

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(f"{dest_folder}")
