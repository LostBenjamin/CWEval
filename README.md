# CWEval

## Setup

```bash
# TODO
```


## Development

### Python (required)

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

# 5. Pull docker image
docker pull co1lin/cweval:latest

# Before running the code, append the repo root path to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```


### C

```bash
mamba install libarchive
sudo apt install libjwt-dev
```


### JavaScript

```bash
# 1. Install nvm according to https://github.com/nvm-sh/nvm?tab=readme-ov-file#install--update-script
# curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# 2. Configure node.js
nvm install --lts
nvm use --lts

# 3. Install dependencies globally
npm install -g escape-html node-rsa argon2 escape-string-regexp lodash js-yaml jsonwebtoken jsdom xpath sqlite3

# 4. Enable global dependencies in scripts
export NODE_PATH=$(npm root -g)
```


### [`pre-commit`](https://pre-commit.com)

[`pre-commit`](https://pre-commit.com) is used to unify the format of all files. Basically after installing it, the linters will check the changed files before each commit. If there is any violation, it will block the commit and fix them. Then you need to `git add` the changes and `git commit` again.
