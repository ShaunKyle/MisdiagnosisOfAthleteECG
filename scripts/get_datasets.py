from pathlib import Path
from os.path import expanduser
import os
import configparser

import git

data_dir = Path(expanduser("./data"))

def wget(url, to_path):
    os.system(f"wget -r -N -c -np -P {to_path} {url}")

# PhysioNet Challenge 2020 - Training data (7.5 GB)
# https://physionet.org/content/challenge-2020/1.0.2/training/#files-panel
#
# Multiple datasets collated in one place:
# - cpsc_2018, 6,877 recordings
# - cpsc_2018_extra (China 12-Lead ECG Challenge Database – unused CPSC 2018 data), 3,453 recordings
# - st_petersburg_incart (12-lead Arrhythmia Database), 74 recordings
# - ptb (Diagnostic ECG Database,) 516 recordings
# - ptb-xl (electrocardiography Database), 21,837 recordings
# - georgia (12-Lead ECG Challenge Database), 10,344 recordings
def download_physionet2020():
    wget(
        url="https://physionet.org/files/challenge-2020/1.0.2/training",
        to_path=data_dir
    )
    print("Finished downloading PhysioNet Challenge 2020 training datasets")

# MIMIC-IV ECG Matched Subset
def download_mimiciv():
    pass

# Norwegian Endurance Athletes (3.2 MB)
# https://physionet.org/content/norwegian-athlete-ecg/1.0.0/
def download_norwegian():
    wget(
        url="https://physionet.org/files/norwegian-athlete-ecg/1.0.0/", 
        to_path=data_dir
    )
    print("Finished downloading norwegian-athlete-ecg")

# Professional Footballers
# https://github.com/dradolfomunoz/PF12RED
# https://pmc.ncbi.nlm.nih.gov/articles/PMC11070232/
# doi: 10.1016/j.dib.2024.110444
def download_pf12red_dataset():
    git.Repo.clone_from(
        url="https://github.com/dradolfomunoz/PF12RED.git",
        to_path=(data_dir / "pf12red")
    )
    print("Finished downloading pf12red")

if __name__ == "__main__":
    # Read current data_dir location from config file, if available.
    config = configparser.ConfigParser()
    if Path("./config.ini").exists():
        config.read("config.ini")
        data_dir = Path(expanduser(config["datasets"]["path"]))

    # Check if user is happy with DATA_DIR location
    while True:
        print(f"DATA_DIR is {data_dir}")
        if input("Change directory? [y/n] ").lower() == "y":
            new_dir = input("Enter new location for DATA_DIR: ")
            data_dir = Path(expanduser(new_dir))
        else:
            break
    if not data_dir.exists():
        data_dir.mkdir()
    
    # Save path to configuration file `config.ini`
    with open("config.ini", 'w') as file:
        file.write("[datasets]\n")
        file.write(f"path: {data_dir}\n")

    # Downloads
    print("Starting downloads...")
    physionet_dir = data_dir / "physionet.org" / "files"
    download_pf12red_dataset() if not (data_dir / "pf12red").exists() else print("pf12red already downloaded")
    download_norwegian() if not (physionet_dir / "norwegian-athlete-ecg").exists() else print("norwegian-athlete-ecg already downloaded")
