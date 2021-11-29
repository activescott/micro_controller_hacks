from hcsr04 import HCSR04
import utime
from constants import MS_PER_SECOND


class DistanceSensor:
    def __init__(self, trigger_pin, echo_pin):
        self._sensor = HCSR04(trigger_pin=trigger_pin, echo_pin=echo_pin)
        print("DistanceSensor: init...")

    def _read_sensor(self):
        samples = const(10)
        total = 0.0
        for c in range(samples):
            total += self._sensor.distance_cm()
        return total / samples

    def _detect_distance_thread(self):
        while True:
            dist = self._read_sensor()
            self.distance(dist)
            utime.sleep_ms(round(MS_PER_SECOND * 0.1))

    def distance(self):
        return self._read_sensor()

    def start(self):
        print("DistanceSensor: start")
