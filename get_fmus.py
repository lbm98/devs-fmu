import os
import subprocess
import requests
from fmpy import extract
from fmpy.util import download_file

from config import REFERENCE_FMUS_PATH


def get_reference_fmus():
    archive_filename = download_file(
        url='https://github.com/modelica/Reference-FMUs/releases/download/v0.0.23/Reference-FMUs-0.0.23.zip',
        checksum='d6ad6fc08e53053fe413540016552387257971261f26f08a855f9a6404ef2991'
    )

    extract(archive_filename, unzipdir=REFERENCE_FMUS_PATH)

    os.remove(archive_filename)


def get_openmodelica_fmus():
    response = requests.get(
        url="https://raw.githubusercontent.com/OpenModelica/OpenModelica/v1.21.0/OMCompiler/Examples/BouncingBall.mo",
    )

    if response.status_code == 200:
        with open('OpenModelica/models/BouncingBall.mo', "wb") as file:
            file.write(response.content)
        print("OpenModelica FMUs download success")
    else:
        print("OpenModelica FMUs download failure")
        exit(1)

    # Maybe use the OMPython Python interface?

    original_directory = os.getcwd()
    os.chdir('OpenModelica/scripts')
    subprocess.run(['omc', 'bouncingBall.mos'])
    os.chdir(original_directory)


if __name__ == '__main__':
    get_reference_fmus()
    get_openmodelica_fmus()
