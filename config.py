import pathlib

REFERENCE_FMUS_DIR = 'Reference-FMUs'
OPENMODELICA_FMUS_DIR = 'OpenModelica/FMUs'

REFERENCE_FMUS_PATH = pathlib.Path(__file__).resolve().parent / REFERENCE_FMUS_DIR
OPENMODELICA_FMUS_PATH = pathlib.Path(__file__).resolve().parent / OPENMODELICA_FMUS_DIR
