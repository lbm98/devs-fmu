#!/bin/bash

set -e

REFERENCE_FMUS_VERSION="0.0.23"

wget -qO Reference-FMUs.zip https://github.com/modelica/Reference-FMUs/releases/download/v0.0.23/Reference-FMUs-${REFERENCE_FMUS_VERSION}.zip
unzip -oq Reference-FMUs.zip -d Reference-FMUs
rm Reference-FMUs.zip

wget -q https://raw.githubusercontent.com/OpenModelica/OpenModelica/v1.21.0/OMCompiler/Examples/BouncingBall.mo
mv BouncingBall.mo OpenModelica/models
cd OpenModelica/scripts
omc bouncingBall.mos
cd ../..
