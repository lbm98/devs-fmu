import os
import shutil
import subprocess
import platform
import urllib.request
import zipfile

from OMPython import OMCSessionZMQ
from jinja2 import Template

from config import (
    REFERENCE_FMUS_VERSION,
    OPENMODELICA_VERSION,
    MODELICA_STANDARD_LIBRARY_VERSION,

    REFERENCE_FMUS_DIR,
    OPENMODELICA_MODELS_DIR,
    OPENMODELICA_BUILD_DIR,
    OPENMODELICA_FMUS_DIR,
    OPENMODELICA_SCRIPTS_DIR
)


def install_reference_fmus():
    urllib.request.urlretrieve(
        url=f"https://github.com/modelica/Reference-FMUs/releases/download/v{REFERENCE_FMUS_VERSION}/Reference-FMUs-{REFERENCE_FMUS_VERSION}.zip",
        filename="Reference-FMUs.zip"
    )

    with zipfile.ZipFile("Reference-FMUs.zip", "r") as zip_ref:
        zip_ref.extractall(REFERENCE_FMUS_DIR)

    os.remove("Reference-FMUs.zip")


def install_openmodelica_bouncing_ball_model():
    urllib.request.urlretrieve(
        url=f"https://raw.githubusercontent.com/OpenModelica/OpenModelica/v{OPENMODELICA_VERSION}/OMCompiler/Examples/BouncingBall.mo",
        filename=OPENMODELICA_MODELS_DIR / "BouncingBall.mo"
    )

    install_openmodelica_model('BouncingBall')


def install_openmodelica_battery_discharge_charge_model():
    # FIXME: We also need to download the models dependencies of the BatteryDischargeCharge model
    urllib.request.urlretrieve(
        url=f"https://raw.githubusercontent.com/modelica/ModelicaStandardLibrary/v{MODELICA_STANDARD_LIBRARY_VERSION}/Modelica/Electrical/Batteries/Examples/BatteryDischargeCharge.mo",
        filename=OPENMODELICA_MODELS_DIR / "BatteryDischargeCharge.mo"
    )

    install_openmodelica_model('BatteryDischargeCharge')


def install_openmodelica_model(model_name: str):
    install_openmodelica_model_with_templated_omc_script(model_name)


def install_openmodelica_model_with_templated_omc_script(model_name: str):
    with open(OPENMODELICA_SCRIPTS_DIR / 'translateModelFMU.mos.template', 'r') as fh:
        template_content = fh.read()

    template = Template(template_content)

    model_file = OPENMODELICA_MODELS_DIR / f'{model_name}.mo'
    build_dir = OPENMODELICA_BUILD_DIR
    fmu_name = OPENMODELICA_FMUS_DIR / f'{model_name}.fmu'

    # Convert paths to use forward slashes,
    # since omc does not like backward slashes in paths
    model_file = model_file.as_posix()
    build_dir = build_dir.as_posix()
    fmu_name = fmu_name.as_posix()

    output = template.render(
        model_file=model_file,
        build_dir=build_dir,
        model_name=model_name,
        fmu_name=fmu_name
    )

    with open(OPENMODELICA_SCRIPTS_DIR / 'translateModelFMU.mos', 'w') as fh:
        fh.write(output)

    if platform.system() == "Windows":
        om_home = os.environ.get('OPENMODELICAHOME')
        om_bin = os.path.join(om_home, 'bin', 'omc')
    else:
        om_bin = 'omc'

    subprocess.call([om_bin, str(OPENMODELICA_SCRIPTS_DIR / 'translateModelFMU.mos')])


def install_openmodelica_model_with_ompython(model_name: str):
    """
    TODO: make OMPython work in Docker
    """
    omc = OMCSessionZMQ()

    load_file = OPENMODELICA_MODELS_DIR / f'{model_name}.mo'
    success = omc.sendExpression(
        f'loadFile("{load_file}")'
    )
    if not success:
        raise Exception(f'Failed to load file: {load_file}')

    # Convert paths to use forward slashes,
    # since omc does not like backward slashes in paths
    cd_dir = OPENMODELICA_BUILD_DIR.as_posix()

    working_directory = omc.sendExpression(
        f'cd("{cd_dir}")'
    )
    if working_directory != cd_dir:
        raise Exception(f'Failed to change directory: {working_directory}')

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


def main():
    install_reference_fmus()
    install_openmodelica_bouncing_ball_model()
    # install_openmodelica_battery_discharge_charge_model()


if __name__ == '__main__':
    main()
