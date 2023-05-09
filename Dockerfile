FROM ubuntu:20.04

# docker build -t devs-fmu .
# docker run -t devs-fmu
# docker run --rm -it --entrypoint bash devs-fmu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        wget \
        git

RUN useradd --create-home --shell /bin/bash dev
USER dev
WORKDIR /home/dev

RUN wget -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-x86_64.sh && \
    sh miniconda.sh -bf && \
    rm miniconda.sh

ENV PATH /home/dev/miniconda3/bin:$PATH

COPY requirements-conda.txt .
RUN conda create --name env
RUN conda shell.bash activate env
RUN conda config --add channels conda-forge
RUN conda install --file requirements-conda.txt

COPY get_fmus.py .
RUN python get_fmus.py

COPY config.py .
COPY devs_fmu devs_fmu
COPY tests tests
RUN pytest
