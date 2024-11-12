FROM co1lin/ubuntu-basic
LABEL maintainer="mail@co1in.me"

# USER ubuntu

# copy build_docker/CWEval to /home/ubuntu/CWEval in the container
COPY --chown=ubuntu:ubuntu build_docker/CWEval /home/ubuntu/CWEval
WORKDIR /home/ubuntu/CWEval

RUN set -ex; source ~/miniforge3/bin/activate; mamba create -y -n cweval python=3.10; rm -rf /home/ubuntu/.cache

# python
RUN set -ex; source ~/miniforge3/bin/activate; conda activate cweval; \
    pip install -r requirements/core.txt; \
    rm -rf /home/ubuntu/.cache

# C
RUN set -ex; source ~/miniforge3/bin/activate; conda activate cweval; \
    mamba install -y libarchive; \
    rm -rf /home/ubuntu/.cache
RUN set -ex; sudo apt update; \
    sudo apt install -y libjwt-dev; \
    rm -rf /home/ubuntu/.cache

# js
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
RUN NVM_CONFIG='export NVM_DIR="$HOME/.nvm"\n[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm\n[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"  # This loads nvm bash_completion' \
    && (grep -qxF "$NVM_CONFIG" ~/.zshrc || echo -e "$NVM_CONFIG" >> ~/.zshrc) \
    && (grep -qxF "$NVM_CONFIG" ~/.bashrc || echo -e "$NVM_CONFIG" >> ~/.bashrc)
RUN set -ex; export NVM_DIR="$HOME/.nvm"; \
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"; \
    nvm install --lts; \
    nvm use --lts; \
    npm install -g escape-html node-rsa argon2 escape-string-regexp lodash js-yaml jsonwebtoken jsdom xpath sqlite3; \
    rm -rf /home/ubuntu/.cache

# golang
RUN set -ex; \
    cd /home/ubuntu; \
    wget https://go.dev/dl/go1.23.3.linux-amd64.tar.gz \
    sudo tar -C /usr/local -xzf go1.23.3.linux-amd64.tar.gz \
    export PATH=$PATH:/usr/local/go/bin \
    cd /home/ubuntu/CWEval; \
    go mod download; \
    rm -rf /home/ubuntu/.cache


CMD [ "zsh" ]
