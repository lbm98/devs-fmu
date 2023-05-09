import os
import shutil
from fmpy import extract
from fmpy.util import download_file

REFERENCE_FMUS_DIR = 'Reference-FMUs'
OPENMODELICA_FMUS_DIR = 'OpenModelica-FMUs'


def get_reference_fmus():
    archive_filename = download_file(
        url='https://github.com/modelica/Reference-FMUs/releases/download/v0.0.23/Reference-FMUs-0.0.23.zip',
        checksum='d6ad6fc08e53053fe413540016552387257971261f26f08a855f9a6404ef2991'
    )

    extract(archive_filename, unzipdir=REFERENCE_FMUS_DIR)

    os.remove(archive_filename)


def get_openmodelica_fmus():
    shutil.copyfile(
        src='/usr/share/doc/omc/testmodels/BouncingBall.mo',
        dst='OPENMODELICA_FMUS_DIR'
    )


if __name__ == '__main__':
    get_reference_fmus()
    get_openmodelica_fmus()

