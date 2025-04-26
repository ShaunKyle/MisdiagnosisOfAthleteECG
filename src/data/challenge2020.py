# Utility functions for extracting labels/demographics from:
# - PhysioNet Challenge 2020 datasets

from src.data.util import diagnosis_codes

from typing import List, TypedDict

import pandas as pd

def extract_snomed_ct_codes_from_comment(dx_comment: str) -> List[int]:
    """Returns a list of SNOMED-CT codes related to ECG diagnoses.

    Assumes that `dx_comment` is in the form "Dx: code1,code2,etc."

    Example usage:
    ```
    record = wfdb.rdheader(ptbxl_dir / "g1" / "HR00001")
    dx_comment = record.comments[2]
    dx_comment
    > 'Dx: 251146004,426783006'

    extract_snomed_ct_codes_from_comment(dx_comment)
    > [251146004, 426783006]
    ```
    """
    # Just the diagnosis codes (ignore the "Dx: " prefix)
    comment = dx_comment.split(': ')[1]

    # Split codes into list, convert to integers
    code_text = comment.split(',')
    return list(map(int, code_text))

class DemographicInfo(TypedDict):
    age: int
    sex: str

def generate_labels_table(records: List[Path]) -> pd.DataFrame:
    """Demographics and binary labels for every record in a PhysioNet Challenge 
    2020 dataset.
    """
    data = []
    for record in records:
        header = wfdb.rdheader(record)

        # Extract demographic info
        age_str = header.comments[0].split(': ')[1]
        age = int( age_str ) if age_str.isnumeric() else None
        sex = header.comments[1].split(': ')[1]
        demographics: DemographicInfo = {
            'age': age,
            'sex': sex,
        }

        # Filter out some records by age (e.g. 300 year old is a typo, kids)
        if not age == None:
            if (age > 90) or (age < 18):
                continue
        
        # Extract ECG diagnostic info (labels)
        diagnoses = extract_snomed_ct_codes_from_comment( header.comments[2] )
        relevant_findings = {
            # Sinus rhythm
            "426177001":  False,  # "Sinus bradycardia",
            "426783006":  False,  # "Normal sinus rhythm",
            "427084000":  False,  # "Sinus tachycardia",
            "427393009":  False,  # "Sinus arrhythmia",

            # Conduction pathway (specifically right bundle branch)
            "713427006":  False,  # "Complete right bundle branch block",
            "713426002":  False,  # "Incomplete right bundle branch block",

            # T-wave (TODO: should be for each lead)
            "164934002":  False,  # "T-wave abnormal",
            "59931005":   False,  # "T-wave inversion",
        }
        for code in diagnoses:
            if code in diagnosis_codes:
                relevant_findings[f"{code}"] = True
        
        # Save data
        data.append( {**demographics, **relevant_findings} )

    return pd.DataFrame(data)