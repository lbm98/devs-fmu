import os
import shutil
import urllib.request
import zipfile

from OMPython import OMCSessionZMQ

from config import (
    REFERENCE_FMUS_VERSION,
    OPENMODELICA_VERSION,
    MODELICA_STANDARD_LIBRARY_VERSION,

    REFERENCE_FMUS_DIR,
    OPENMODELICA_MODELS_DIR,
    OPENMODELICA_BUILD_DIR,
    OPENMODELICA_FMUS_DIR
)


def install_reference_fmus():
    urllib.request.urlretrieve(
        url=f"https://github.com/modelica/Reference-FMUs/releases/download/v{REFERENCE_FMUS_VERSION}/Reference-FMUs-{REFERENCE_FMUS_VERSION}.zip",
        filename="Reference-FMUs.zip"
    )

    with zipfile.ZipFile("Reference-FMUs.zip", "r") as zip_ref:
        zip_ref.extractall(REFERENCE_FMUS_DIR)

    os.remove("Reference-FMUs.zip")


def install_bouncing_ball_model():
    urllib.request.urlretrieve(
        url=f"https://raw.githubusercontent.com/OpenModelica/OpenModelica/v{OPENMODELICA_VERSION}/OMCompiler/Examples/BouncingBall.mo",
        filename=OPENMODELICA_MODELS_DIR / "BouncingBall.mo"
    )

    install_openmodelica_model('BouncingBall')


def install_battery_example_model():
    # FIXME: Need to also download the models that BatteryDischargeCharge depends on
    urllib.request.urlretrieve(
        url=f"https://raw.githubusercontent.com/modelica/ModelicaStandardLibrary/v{MODELICA_STANDARD_LIBRARY_VERSION}/Modelica/Electrical/Batteries/Examples/BatteryDischargeCharge.mo",
        filename=OPENMODELICA_MODELS_DIR / "BatteryDischargeCharge.mo"
    )

    install_openmodelica_model('BatteryDischargeCharge')


def install_openmodelica_model(model_name: str):
    omc = OMCSessionZMQ()

    load_file_dir = OPENMODELICA_MODELS_DIR / f'{model_name}.mo'
    success = omc.sendExpression(
        f'loadFile("{load_file_dir}")'
    )
    if not success:
        raise Exception(f'Failed to load file: {load_file_dir}')

    omc.sendExpression(
        f'cd("{OPENMODELICA_BUILD_DIR}")'
    )

    omc.sendExpression(
        f'translateModelFMU('
        f'  className={model_name},'
        f'  version="2.0",'
        f'  fmuType="cs"'
        f')'
    )

    shutil.copy(
        src=OPENMODELICA_BUILD_DIR / f'{model_name}.fmu',
        dst=OPENMODELICA_FMUS_DIR
    )


if __name__ == '__main__':
    # install_reference_fmus()
    # install_bouncing_ball_model()
    install_battery_example_model()
