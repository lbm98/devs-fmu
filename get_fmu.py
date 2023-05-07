import os
from fmpy import extract
from fmpy.util import download_file

UNZIPDIR = 'fmu'


def main():
    archive_filename = download_file(
        url='https://github.com/modelica/Reference-FMUs/releases/download/v0.0.23/Reference-FMUs-0.0.23.zip',
        checksum='d6ad6fc08e53053fe413540016552387257971261f26f08a855f9a6404ef2991'
    )

    extract(archive_filename, unzipdir=UNZIPDIR)

    os.remove(archive_filename)


if __name__ == '__main__':
    main()
