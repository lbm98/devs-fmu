import sys
from datetime import timedelta

from devs_fmu.simulator import simulator
from devs_fmu.bouncing_ball import BouncingBall


def test_bouncing_ball():
    BouncingBall()


def test_bouncing_ball_initial_values():
    m = BouncingBall()
    assert m.get_height() == 1
    assert m.get_velocity() == 0


def test_bouncing_ball_with_simulation():
    m = BouncingBall()

    simulator.stop(timedelta(seconds=3))
    simulator.run()

    assert m.get_height() == sys.float_info.min
    assert m.get_velocity() == 0


def test_bouncing_ball_with_state_change():
    m = BouncingBall()

    def change_height(bouncing_ball):
        bouncing_ball.set_height(1)

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