from datetime import timedelta
from devs_fmu.simulator import simulator


def test_simulator_run():
    called_f1 = None
    called_f2 = None

    def f1():
        nonlocal called_f1
        called_f1 = simulator.now

    def f2():
        nonlocal called_f2
        called_f2 = simulator.now

    simulator.schedule(
        timedelta(seconds=1),
        f1
    )

    simulator.schedule(
        timedelta(seconds=2),
        f2
    )

    simulator.run()

    assert called_f1 == timedelta(seconds=1)
    assert called_f2 == timedelta(seconds=2)


def test_simulator_advance():
    called_f1 = None
    called_f2 = None

    def f1():
        nonlocal called_f1
        called_f1 = simulator.now

    def f2():
        nonlocal called_f2
        called_f2 = simulator.now

    simulator.schedule(
        timedelta(seconds=1),
        f1
    )

    simulator.schedule(
        timedelta(seconds=2),
        f2
    )

    for i in range(4):
        simulator.advance(timedelta(seconds=0.5))

    assert called_f1 == timedelta(seconds=1)
    assert called_f2 == timedelta(seconds=2)
