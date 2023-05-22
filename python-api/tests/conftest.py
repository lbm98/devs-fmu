import sys
import pytest
from pathlib import Path

from devs_fmu.simulator import simulator

SOURCES_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(SOURCES_ROOT))
sys.path.append(str(CONFIG_DIR))


@pytest.fixture(autouse=True)
def cleanup():
    # reset simulator after each test
    simulator.reset()
