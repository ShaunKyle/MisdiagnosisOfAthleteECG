from pathlib import Path
from zipfile import ZipFile

import requests

sources_url = "https://physionet.org/static/published-projects/challenge-2020/1.0.2/sources/"
destination_dir = Path("./entries")

# Add the names of teams to download entries of. See challenge results table:
# https://moody-challenge.physionet.org/2020/results/
teams = [
    "Prna",
    "DSAIL_SNU",
]

def download_zip(url, save_path):
    print(f"Downloading file from: {url}")
    response = requests.get(url, stream=True)  # Stream the response to handle large files
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):  
                file.write(chunk)
        print(f"File downloaded successfully: {save_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def extract_zip(file, out_dir):
    with ZipFile(file, 'r') as zip:
        zip.extractall(out_dir)

if __name__ == '__main__':
    # Make sure destination directory exists
    destination_dir.mkdir(parents=True, exist_ok=True)

    # Obtain each team's entry
    for name in teams:
        destination_file = destination_dir / (name + ".zip")

        # Download zip folder with team's entry
        if destination_file.exists():
            print(f"Already downloaded: {destination_file}")
        else:
            url = sources_url + name + ".zip"
            download_zip(url, destination_file)

        # Extract zip folder
        extract_zip(destination_file, destination_dir)
