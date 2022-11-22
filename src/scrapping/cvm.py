import os
import zipfile

import requests

from src.scrapping.checks import check_already_downloaded


def download_unzip(url: str, dest_folder: str) -> None:
    """Downloads and unzips file from target url to destination folder.

    Args:
        url (str): URL of the target file to be downloaded.
        dest_folder (str): Path to destination folder where file should be unziped.
    """
    print("Downloading the file...")
    file_name = download_file(url, dest_folder)
    print("Unzipping the file...")
    unzip_file(file_name, dest_folder=file_name[:-4])
    print(f"File {file_name} successfuly downloaded to {dest_folder}!")


def create_if_not_dir(dest_folder: str) -> None:
    """Creates a directory in dest_folder PATH if it doesn't exist yet.

    Args:
        dest_folder (str): Path to destination folder.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)


def download_file(url: str, dest_folder: str) -> str:
    """Downloads file from a specified URL to a specified destination folder.

    Args:
        url (str): URL with the file to be downloaded.
        dest_folder (str): Path of the destination folder.

    Returns:
        str: File path of the downloaded file.
    """
    create_if_not_dir(dest_folder)

    filename = url.split("/")[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)
    if check_already_downloaded(file_path):
        print(f"Error: File {os.path.abspath(file_path)} already exists.")
        return file_path
    r = requests.get(url, stream=True)

    if r.ok:
        print(f"Success: Saving to {os.path.abspath(file_path)}")
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        print(f"Error: Download failed status code {r.status_code}\n{r.text}")
    return file_path


def unzip_file(file_path: str, dest_folder: str):
    """Unzips a .zip file to a specified destination folder.

    Args:
        file_path (str): Path of the .zip file.
        dest_folder (str): Destination folder where the unziped files should be stored.
    """
    create_if_not_dir(dest_folder)
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(f"./{dest_folder}")

