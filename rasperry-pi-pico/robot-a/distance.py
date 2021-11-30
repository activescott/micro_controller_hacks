from hcsr04 import HCSR04
import utime
from constants import MS_PER_SECOND


class DistanceSensor:
    def __init__(self, trigger_pin, echo_pin):
        self._sensor = HCSR04(trigger_pin=trigger_pin, echo_pin=echo_pin)
        print("DistanceSensor: init...")

    def _read_sensor(self):
        # I don't know why but regularly this sensor returns readings aproximately at ~0.79 that are nonsensical. Averaging definitely gets rid of most of them
        samples = const(10)
        total = 0.0
        readings = [self._sensor.distance_cm() for r in range(samples)]
        #if min(readings) < 1:
        #    print("\nhcsr04: at least one reading less than 1:{}\n".format(readings))
        return sum(readings) / len(readings)

    def distance(self):
        return self._read_sensor()

    def start(self):
        print("DistanceSensor: start")
