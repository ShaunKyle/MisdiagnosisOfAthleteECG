from pathlib import Path
from typing import List

import pandas as pd

diagnosis_codes = {
    # Sinus rhythm
    426177001:  "Sinus bradycardia",
    426783006:  "Normal sinus rhythm",
    427084000:  "Sinus tachycardia",
    427393009:  "Sinus arrhythmia",

    # Conduction pathway (specifically right bundle branch)
    713427006:  "Complete right bundle branch block",
    713426002:  "Incomplete right bundle branch block",

    # T-wave (should be for each lead)
    164934002:  "T-wave abnormal",
    59931005:   "T-wave inversion",
}

def get_all_records(dataset_dir: Path) -> List[Path]:
    """Returns a list of every record in a PhysioNet-style dataset

    Can handle 1 level of nesting.
    """
    records = []
    for item in dataset_dir.iterdir():
        # a) Search folder
        # (e.g. PhysioNet Challenge datasets are divided into g1/, g2/, etc.)
        if item.is_dir():
            # For every record (each record has a `.hea` header file)
            for file in item.iterdir():
                if file.suffix == '.hea':
                    records.append( item / file.stem )
        # b) Check if file is record
        elif item.is_file():
            if item.suffix == '.hea':
                records.append( item.stem )
    return records

def get_predicted_labels(file) -> List[int]:
    """Get model predictions PhysioNet 2020 challenge ouput CSV file.
    
    Returns list of SNOMED-CT diagnosis codes.
    """
    csv = pd.read_csv(file, header=1)
    # csv.loc[0] -> Binary prediction after threshold applied (true or false)
    # csv.loc[1] -> Probability of finding

    predicted_labels = []
    for code in diagnosis_codes:
        if csv.loc[0][f"{code}"] == 1:
            predicted_labels.append(code)
    
    return predicted_labels
