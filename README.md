# Classification of 12-lead ECG recordings from athletes

> Investigating reduced deep learning model performance on athletic patient 
cohorts

Running 12-Lead ECG classification models from the [2020 George B. Moody 
PhysioNet Challenge](https://moody-challenge.physionet.org/2020/results/) on 
someone else's computer with a bigger GPU than mine.

In addition to the original datasets used in the 2020 PhysioNet Challenge, this 
project also tests the models on a unique patient cohort: professional 
athletes. 

Reports (hosted by [nbsanity](https://www.answer.ai/posts/2024-12-13-nbsanity.html)):
- [Misclassification of athlete ECG by GE Marquette SL12 algorithm](https://nbsanity.com/ShaunKyle/PhysioNetChallenge2020/blob/main/nbs/Marquette-SL12-misclassification.ipynb)
- TODO: Measuring shift in population between datasets
- TODO: Verify model performance on 2020 PhysioNet Challenge datasets
- TODO: Reduced model performance on athletic datasets

## Setup

Create python virtual environment inside the `.venv` directory.

```sh
uv venv --python 3.10
```

Activate the virutal environment in shell (prepend `.venv/bin` to PATH)

```sh
# On MacOS, Linux, or other POSIX
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

Install (or update) dependencies

```sh
# On computer with CUDA 11.6
uv pip install -U -r requirements-CUDA.txt
uv pip install -U -r requirements.txt

# On other computers (uses CPU)
uv pip install -U -r requirements-CPU.txt
uv pip install -U -r requirements.txt
```

## Citation

Citation metadata is provided by [CITATION.cff](./CITATION.cff). For convenience, a BibTex citation is provided below.

```bibtex
@software{Kyle_Classification_of_12-lead,
author = {Kyle, Shaun},
title = {{Classification of 12-lead ECG recordings from athletes}},
url = {https://github.com/ShaunKyle/PhysioNetChallenge2020}
}
```
