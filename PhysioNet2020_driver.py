from pathlib import Path
import numpy as np, os, sys
from wfdb import rdrecord
from src.run_12ECG_classifier import load_12ECG_model, run_12ECG_classifier

def load_challenge_data(filepath: Path):
    record = rdrecord(filepath)
    data = record.p_signal.transpose()

    headerpath = filepath.with_suffix('.hea')
    with open(headerpath,'r') as f:
        header_data=f.readlines()

    return data, header_data


def save_challenge_predictions(output_directory: Path, filename: str, scores,labels,classes):
    output_file = os.path.join(output_directory / (filename+".csv"))

    # Include the filename as the recording number
    recording_string = '#{}'.format(filename)
    class_string = ','.join(classes)
    label_string = ','.join(str(i) for i in labels)
    score_string = ','.join(str(i) for i in scores)

    with open(output_file, 'w') as f:
        f.write(recording_string + '\n' + class_string + '\n' + label_string + '\n' + score_string + '\n')



if __name__ == '__main__':
    # Parse arguments.
    if len(sys.argv) != 5:
        raise Exception('Include the input and output directories as arguments, e.g., python driver.py model_input model_config input output.')

    model_input = sys.argv[1]
    model_config = Path(sys.argv[2])
    input_directory = Path(sys.argv[3])
    output_directory = Path(sys.argv[4])

    # Find files.
    input_files = []
    for f in input_directory.iterdir():
        if f.suffix == ".hea":
            input_files.append(f.stem)
    
    if not output_directory.exists():
        output_directory.mkdir()

    # Load model.
    print('Loading 12ECG model...')
    model = load_12ECG_model(model_input, model_config)

    # Iterate over files.
    print('Extracting 12ECG features...')
    num_files = len(input_files)

    for i, f in enumerate(input_files):
        print('    {}/{}...'.format(i+1, num_files))
        data,header_data = load_challenge_data( input_directory / f )
        current_label, current_score,classes = run_12ECG_classifier(data,header_data, model)
        # Save results.
        save_challenge_predictions(output_directory,f,current_score,current_label,classes)


    print('Done.')
