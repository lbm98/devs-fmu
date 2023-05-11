import sys
import pytest
from pathlib import Path

from devs_fmu.simulator import simulator

SOURCES_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(SOURCES_ROOT))


@pytest.fixture(autouse=True)
def cleanup():
    # reset simulator after each test
    simulator.reset()
