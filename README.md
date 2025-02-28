# Classification of 12-lead ECGs

Running 12-Lead ECG classification models from the [2020 George B. Moody 
PhysioNet Challenge](https://moody-challenge.physionet.org/2020/results/) on 
someone else's computer.

## Setup

Create python virtual environment inside the `.venv` directory.

```sh
uv venv --python 3.12
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
