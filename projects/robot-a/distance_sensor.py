from hcsr04 import HCSR04
import utime
from constants import MS_PER_SECOND, DISTANCE_SENSOR_TRIGGER_PIN, DISTANCE_SENSOR_ECHO_PIN


_singleton: HCSR04 = None


def init():
    print("distance sensor starting...")
    global _singleton
    _singleton = HCSR04(trigger_pin=DISTANCE_SENSOR_TRIGGER_PIN,
                        echo_pin=DISTANCE_SENSOR_ECHO_PIN)
    print("distance sensor started.")


def deinit():
    pass


def distance():
    # I don't know why but regularly this sensor returns readings approximately at ~0.79 that are nonsensical. Averaging definitely gets rid of most of them
    samples = const(10)
    total = 0.0
    readings = [_singleton.distance_cm() for r in range(samples)]
    # if min(readings) < 1:
    #    print("\nhcsr04: at least one reading less than 1:{}\n".format(readings))
    return sum(readings) / len(readings)
