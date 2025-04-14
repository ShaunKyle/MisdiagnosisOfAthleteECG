import configparser
import shutil
import sys
from pathlib import Path
from zipfile import ZipFile

if __name__ == "__main__":
    # Import configuration settings, like location of data directory.
    config = configparser.ConfigParser()
    if not Path("config.ini").exists():
        print("WARNING: Please generate a config.ini file by running scripts/get_datasets.py")
        sys.exit()
    else:
        config.read("config.ini")
        data_dir = Path((config["datasets"]["path"])).expanduser()
        print(f"Datasets are located at {data_dir.resolve()}")
    
    # Extract source code and weights from zip file
    model_zip_dir = data_dir / "challenge-2020" / "1.0.2" / "sources"
    with ZipFile(model_zip_dir / "DSAIL_SNU.zip", 'r') as zip:
        zip.extractall(model_zip_dir)
    team_dir = model_zip_dir / "DSAIL_SNU" / "PhysioNetChallenge2020_DSAIL_SNU7"
    
    # To make it easier to run and modify the model, we'll copy the source code 
    # and model weights to the root of our git repo.
    #
    # We'll copy the following directories from `model_dir` to the root of our git repo:
    # - `config` (includes confusion matrix weights, settings for data preprocessing etc.)
    # - `output_training_directory` (checkpoints for model weights)
    #
    # ASSUMPTION: Script is run from project root directory

    # Checkpoints for model weights
    result = shutil.copytree(team_dir / "output_training_directory", Path.cwd() / "checkpoints" / "original", dirs_exist_ok=True)
    print(result)

    # Model configuration
    # Don't want to overwrite if we make changes to config later on.
    try:
        shutil.copytree(team_dir / "config", Path.cwd() / "config", dirs_exist_ok=False)
    except FileExistsError:
        print("config directory already exists")
