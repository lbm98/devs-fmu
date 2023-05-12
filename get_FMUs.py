import os
import urllib.request
import zipfile

REFERENCE_FMUS_VERSION = "0.0.23"
OPENMODELICA_VERSION = "1.21.0"
MODELICA_STANDARD_LIBRARY_VERSION = "4.0.0"


def install_reference_fmus():
    urllib.request.urlretrieve(
        url=f"https://github.com/modelica/Reference-FMUs/releases/download/v{REFERENCE_FMUS_VERSION}/Reference-FMUs-{REFERENCE_FMUS_VERSION}.zip",
        filename="Reference-FMUs.zip"
    )

    with zipfile.ZipFile("Reference-FMUs.zip", "r") as zip_ref:
        zip_ref.extractall("Reference-FMUs")

    os.remove("Reference-FMUs.zip")


def install_openmmodelica_fmus():
    urllib.request.urlretrieve(
        url=f"https://raw.githubusercontent.com/OpenModelica/OpenModelica/v{OPENMODELICA_VERSION}/OMCompiler/Examples/BouncingBall.mo",
        filename="OpenModelica/models/BouncingBall.mo"
    )

    os.chdir("OpenModelica/scripts")
    os.system("omc bouncingBall.mos")


if __name__ == '__main__':
    install_reference_fmus()
    install_openmmodelica_fmus()
