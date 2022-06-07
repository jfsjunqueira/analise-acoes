import os
import requests
import zipfile
from checks import check_already_downloaded

def download_file(url: str, dest_folder: str) -> str:
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)
    if check_already_downloaded(file_path):
        print(f"Error: File {os.path.abspath(file_path)} already exists.")
        return file_path
    r = requests.get(url, stream=True)
    
    if r.ok:
        print(f"Success: Saving to {os.path.abspath(file_path)}")
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print(f"Error: Download failed status code {r.status_code}\n{r.text}")
    return file_path
        
def unzip_file(file_path:str, dest_folder:str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(f'./{dest_folder}')