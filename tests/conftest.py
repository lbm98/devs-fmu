from devs_fmu.simulator import simulator
import pytest


@pytest.fixture(autouse=True)
def cleanup():
    # reset simulator after each test
    simulator.reset()
