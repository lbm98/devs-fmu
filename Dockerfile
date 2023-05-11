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

###############################
# INSTALL OPENMODELICA
###############################

# https://github.com/OpenModelica/OpenModelicaDockerImages/blob/v1.21.0/Dockerfile

RUN echo "deb https://build.openmodelica.org/omc/builds/linux/releases/${OPENMODELICA_VERSION}/ `cat /etc/lsb-release | grep CODENAME | cut -d= -f2` release" > /etc/apt/sources.list.d/openmodelica.list && \
    wget https://build.openmodelica.org/apt/openmodelica.asc -O- | apt-key add -

RUN apt-get update && \
    apt-get install -qy --no-install-recommends \
        omc && \
    apt-get clean

###############################
# INSTALL CMAKE
###############################

# https://github.com/actions/runner-images/blob/main/images/linux/scripts/installers/cmake.sh

RUN wget -O cmakeinstall.sh https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-linux-x86_64.sh && \
    chmod +x cmakeinstall.sh && \
    ./cmakeinstall.sh --prefix=/usr/local --exclude-subdir && \
    rm cmakeinstall.sh

###############################
# SWITCH TO USER
###############################

RUN useradd --create-home --shell /bin/bash dev
USER dev
WORKDIR /home/dev

###############################
# INSTALL MINICONDA
###############################

RUN wget -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    sh miniconda.sh -bf && \
    rm miniconda.sh

ENV PATH /home/dev/miniconda3/bin:$PATH

###############################
# SETUP PYTHON API ENV
###############################

COPY python-api/envs/test-environment.yml test-environment.yml
RUN conda env create -f test-environment.yml

###############################
# SETUP C API ENV
###############################

COPY c-api/envs/environment.yml c-api-environment.yml
RUN conda env create -f c-api-environment.yml

###############################
# COPY PROJECT
###############################

RUN mkdir project
WORKDIR project

COPY --chown=dev . .

###############################
# TEST PYTHON API
###############################

RUN ./get_FMUs.sh
RUN conda run -n devs-fmu-test pytest python-api

###############################
# TEST C API
###############################

WORKDIR c-api
RUN ./fetch.sh
RUN mkdir build
WORKDIR build
RUN cmake ..
RUN cmake --build . --target run-c-api