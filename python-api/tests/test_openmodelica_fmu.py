from datetime import timedelta

from devs_fmu.simulator import simulator
from devs_fmu.bouncing_ball import BouncingBall

from config import OPENMODELICA_FMUS_DIR

FMU_PATH = OPENMODELICA_FMUS_DIR / 'BouncingBall.fmu'


def test_bouncing_ball():
    BouncingBall(FMU_PATH)


def test_bouncing_ball_init():
    m = BouncingBall(FMU_PATH)

    assert m.height == 1
    assert m.velocity == 0

    assert m.value_references == {
        'h': 0,
        'v': 1
    }


def test_bouncing_ball_simulated():
    simulator.reset()
    m = BouncingBall(FMU_PATH)

    simulator.advance(timedelta(seconds=1))

    # TODO: handle the numeric instability
    # assert m.get_height() < 1.0
