import sys
from datetime import timedelta

from devs_fmu.simulator import simulator
from devs_fmu.bouncing_ball import BouncingBall

from config import REFERENCE_FMUS_DIR

FMU_PATH = REFERENCE_FMUS_DIR / '2.0/BouncingBall.fmu'


def test_bouncing_ball():
    BouncingBall(FMU_PATH)


def test_bouncing_ball_init():
    m = BouncingBall(FMU_PATH)

    assert m.height == 1
    assert m.velocity == 0

    assert m.value_references == {
        'h': 1,
        'v': 3
    }


def test_bouncing_ball_simulated():
    m = BouncingBall(FMU_PATH)

    simulator.stop(timedelta(seconds=3))
    simulator.run()

    assert m.get_height() == sys.float_info.min
    assert m.get_velocity() == 0


def test_bouncing_ball_simulated_with_state_change():
    m = BouncingBall(FMU_PATH)

    def change_height(m):
        m.set_height(1)

    simulator.schedule(
        timedelta(seconds=1),
        change_height,
        m
    )

    assert m.get_height() == 1
    assert m.get_velocity() == 0

    simulator.advance(timedelta(seconds=0.5))

    assert m.get_height() < 1

    simulator.advance(timedelta(seconds=0.5))

    assert m.get_height() == 1

    simulator.advance(timedelta(seconds=2))

    assert m.get_height() == sys.float_info.min
    assert m.get_velocity() == 0
