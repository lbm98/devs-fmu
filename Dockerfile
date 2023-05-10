FROM ubuntu:20.04

# docker build -t devs-fmu .
# docker run -t devs-fmu
# docker run --rm -it --entrypoint bash devs-fmu

ENV OPENMODELICA_VERSION=1.21.0

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -qy \
        build-essential \
        wget \
        gnupg \
        ca-certificates \
        git && \
    apt-get clean

# https://github.com/OpenModelica/OpenModelicaDockerImages/blob/v1.21.0/Dockerfile

RUN echo "deb https://build.openmodelica.org/omc/builds/linux/releases/$OPENMODELICA_VERSION/ `cat /etc/lsb-release | grep CODENAME | cut -d= -f2` release" > /etc/apt/sources.list.d/openmodelica.list && \
    wget https://build.openmodelica.org/apt/openmodelica.asc -O- | apt-key add -

RUN apt-get update && \
    apt-get install -qy --no-install-recommends \
        omc && \
    apt-get clean

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

RUN mkdir project
WORKDIR project

COPY --chown=dev . .

RUN python get_fmus.py
RUN pytest
