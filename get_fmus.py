import os
import subprocess
from fmpy import extract
from fmpy.util import download_file

from config import REFERENCE_FMUS_DIR


def get_reference_fmus():
    archive_filename = download_file(
        url='https://github.com/modelica/Reference-FMUs/releases/download/v0.0.23/Reference-FMUs-0.0.23.zip',
        checksum='d6ad6fc08e53053fe413540016552387257971261f26f08a855f9a6404ef2991'
    )

    extract(archive_filename, unzipdir=REFERENCE_FMUS_DIR)

    os.remove(archive_filename)


def get_openmodelica_fmus():
    # Maybe make the .OpenModelica-Scripts file a template to avoid hard-coding the directory name?
    subprocess.run(['omc', 'OpenModelica-Scripts/bouncingBall.mos'])


if __name__ == '__main__':
    get_reference_fmus()
    get_openmodelica_fmus()
