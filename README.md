# CWEval

## Setup

```bash
# TODO
```


## Development

```bash
# 1. Setup mamba/conda (mamba resolves dependencies faster than conda).
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh

# 2. Create a Python environment
mamba create -y -n cweval python=3.10
conda activate cweval

# 3. Install core dependencies
pip install -r requirements/core.txt

# 4. Setup dependencies for development
pip install -r requirements/dev.txt
pre-commit install

# 6. Install dependencies for evaluation
pip install -r requirements/eval.txt

# Before running the code, append the repo root path to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### [`pre-commit`](https://pre-commit.com)

[`pre-commit`](https://pre-commit.com) is used to unify the format of all files. Basically after installing it, the linters will check the changed files before each commit. If there is any violation, it will block the commit and fix them. Then you need to `git add` the changes and `git commit` again.
