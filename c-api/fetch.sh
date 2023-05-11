#!/bin/bash

set -e

REFERENCE_FMUS_VERSION="0.0.23"

rm -rf Reference-FMUs

git clone --depth=1 --branch v${REFERENCE_FMUS_VERSION} https://github.com/modelica/Reference-FMUs
cd Reference-FMUs
git apply ../patches/*.patch
rm -rf .git

cd ThirdParty

conda run -n devs-fmu-c-api python build_cvode.py
conda run -n devs-fmu-c-api python build_libxml2.py
conda run -n devs-fmu-c-api python build_zlib.py