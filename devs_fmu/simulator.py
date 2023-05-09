import heapq
from dataclasses import dataclass
from datetime import timedelta
from typing import Callable, Any


@dataclass
class Event:
    time: timedelta
    handler: Callable
    args: tuple[Any, ...]

    def __lt__(self, other: 'Event') -> bool:
        return self.time < other.time


class Simulator:
    def __init__(self):
        self.events: list[Event] = []
        self.time = timedelta()
        self.stop_time: timedelta | None = None

    def schedule(self, delay: timedelta, handler: Callable, *args: Any):
        absolute_time = self.time + delay
        event = Event(absolute_time, handler, args)
        heapq.heappush(self.events, event)

    def schedule_now(self, handler: Callable, *args: Any):
        return self.schedule(self.time, handler, *args)

    def run(self):
        while True:
            if len(self.events) == 0:
                if self.stop_time is not None:
                    self.time = self.stop_time
                return

            event = heapq.heappop(self.events)
            self.time = event.time

            # If the stop condition is at x seconds,
            # we choose to still process all events scheduled at x seconds,
            # therefore the strict inequality
            if self.stop_time is not None and self.time > self.stop_time:

                # Do not discard the event
                heapq.heappush(self.events, event)
                self.time = self.stop_time
                return

            event.handler(*event.args)

    def stop(self, stop_time: timedelta):
        """ Relative soft stop """
        self.stop_time = self.time + stop_time

    def advance(self, time: timedelta):
        """ Relative advance """
        self.stop(time)
        self.run()

    def reset(self):
        self.events = []
        self.time = timedelta(0)

    @property
    def now(self) -> timedelta:
        return self.time


simulator = Simulator()
