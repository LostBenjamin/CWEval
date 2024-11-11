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

RUN sudo apt update && apt install -y libjwt-dev; rm -rf /home/ubuntu/.cache

CMD [ "zsh" ]
