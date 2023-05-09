import shutil
from datetime import timedelta

from fmpy import (
    extract,
    supported_platforms,
    platform as current_platform,
    read_model_description,
    instantiate_fmu
)
from fmpy.fmi2 import FMU2Slave

from .simulator import simulator
from config import FMU_ROOT


class BouncingBall:
    def __init__(self):
        self.fmu: FMU2Slave | None = None
        self.fmu_dir = None

        # Maybe get these vales from the model description?
        self.height = 1.0
        self.velocity = 0.0

        self.last_update_time = timedelta(0)

        # Maybe get these vales from the model description?
        self.value_references = {
            'h': 1,
            'v': 3,
            'e': 6
        }

        self.initialize()

    def initialize(self):
        # Extract the FMU to a temporary directory
        self.fmu_dir = extract(FMU_ROOT / '2.0/BouncingBall.fmu')

        # Check if the platform is supported
        platforms = supported_platforms(self.fmu_dir)
        if current_platform not in platforms:
            raise Exception('The current platform is not supported by the FMU')

        # Parse the model description
        model_description = read_model_description(self.fmu_dir)

        # Check if FMI type is Co-Simulation
        if model_description.coSimulation is None:
            raise Exception('The FMI type must be Co-Simulation')
        fmi_type = 'CoSimulation'

        # Instantiate the FMU
        self.fmu = instantiate_fmu(
            unzipdir=self.fmu_dir,
            model_description=model_description,
            fmi_type=fmi_type
        )

        # Set the start and stop time of the simulation
        # Setting stopTime to None makes the simulation run indefinitely
        self.fmu.setupExperiment(
            startTime=0.0,
            stopTime=None
        )

        self.fmu.enterInitializationMode()
        self.fmu.exitInitializationMode()

    def __del__(self):
        self.fmu.freeInstance()
        shutil.rmtree(self.fmu_dir)

    def set_height(self, h: float):
        self.fmu.setReal(
            vr=[self.value_references['h']],
            value=[h]
        )

    def set_velocity(self, v: float):
        self.fmu.setReal(
            vr=[self.value_references['v']],
            value=[v]
        )

    def set_attenuation_factor(self, e: float):
        self.fmu.setReal(
            vr=[self.value_references['e']],
            value=[e]
        )

    def _get_internal_height(self) -> float:
        return self.fmu.getReal([self.value_references['h']])[0]

    def _get_internal_velocity(self) -> float:
        return self.fmu.getReal([self.value_references['v']])[0]

    def update_if_necessary(self) -> (float | None, bool):
        # Do a sanity check
        assert self.last_update_time <= simulator.now

        # Check if an update is necessary
        if self.last_update_time != simulator.now:

            # Here, an update is necessary
            step_size = simulator.now - self.last_update_time

            self.fmu.doStep(
                currentCommunicationPoint=simulator.now.total_seconds(),
                communicationStepSize=step_size.total_seconds(),
            )

            self.height = self._get_internal_height()
            self.velocity = self._get_internal_velocity()

            self.last_update_time = simulator.now
            updated = True
        else:
            # Here, an update is NOT necessary
            updated = False

        return updated

    def get_height(self) -> float:
        self.update_if_necessary()
        return self.height

    def get_velocity(self) -> float:
        self.update_if_necessary()
        return self.velocity
