FROM ubuntu:20.04

# docker build -t devs-fmu .
# docker run -t devs-fmu
# docker run --rm -it --entrypoint bash devs-fmu

ENV OPENMODELICA_VERSION="1.21.0"
ENV MINICONDA_VERSION="py310_23.3.1-0"
ENV CMAKE_VERSION="3.26.3"

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

RUN echo "deb https://build.openmodelica.org/omc/builds/linux/releases/${OPENMODELICA_VERSION}/ `cat /etc/lsb-release | grep CODENAME | cut -d= -f2` release" > /etc/apt/sources.list.d/openmodelica.list && \
    wget https://build.openmodelica.org/apt/openmodelica.asc -O- | apt-key add -

RUN apt-get update && \
    apt-get install -qy --no-install-recommends \
        omc && \
    apt-get clean

# https://github.com/actions/runner-images/blob/main/images/linux/scripts/installers/cmake.sh

RUN wget -O cmakeinstall.sh https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-linux-x86_64.sh && \
    chmod +x cmakeinstall.sh && \
    ./cmakeinstall.sh --prefix=/usr/local --exclude-subdir && \
    rm cmakeinstall.sh

RUN useradd --create-home --shell /bin/bash dev
USER dev
WORKDIR /home/dev

RUN wget -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    sh miniconda.sh -bf && \
    rm miniconda.sh

ENV PATH /home/dev/miniconda3/bin:$PATH

COPY python-api/test-environment.yml test-environment.yml
RUN conda env create -f test-environment.yml

RUN mkdir project
WORKDIR project

COPY --chown=dev . .

RUN ./get_FMUs.sh
RUN conda run -n devs-fmu-test pytest python-api
