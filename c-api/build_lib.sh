#!/bin/bash

set -e

REFERENCE_FMUS_VERSION="0.0.23"

cd lib

rm -rf Reference-FMUs

git clone --depth=1 --branch v${REFERENCE_FMUS_VERSION} https://github.com/modelica/Reference-FMUs
cd Reference-FMUs
git apply ../patches/*.patch
rm -rf .git

cd ThirdParty
python build_cvode.py
python build_libxml2.py
python build_zlib.py
cd ..

mkdir build
cd build
cmake .. -DWITH_FMUSIM=TRUE
cmake --build . --target fmusim

mv fmusim/libfmusim_lib.a ..
