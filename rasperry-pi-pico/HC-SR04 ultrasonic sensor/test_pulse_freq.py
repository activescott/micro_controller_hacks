# The HC-SR04 ultrasonic sensor sometimes returns a few nonsensical <1cm readings. I suspect maybe due to echo. So doing some testing here to see how nonsensical readings we get at different intervals.
# TLDR: NO DIFFERENCE even at 0ms
# So... this must just be because of environmental echo (shapes of things and angles causing echo)
from hcsr04 import HCSR04
import utime

TRIGGER_PIN = 2
ECHO_PIN = 3

sensor = HCSR04(trigger_pin=TRIGGER_PIN, echo_pin=ECHO_PIN)


def log(msg):
    tt = utime.localtime()[3:6]
    prefix = "{:02d}:{:02d}.{:02d} ".format(*tt)
    print(prefix + msg)


#counter = 10**4
# while counter > 0:
#  counter -= 1
#  utime.sleep(0.5)
# distance = sensor.distance_cm()
# log("{} cm".format(distance))

frequencies_in_ms = range(0, 200, 1)
samples = 10

for freq in frequencies_in_ms:
    readings = []
    for x in range(samples):
        distance = sensor.distance_cm()
        readings.append(distance)
        if freq > 0:
            utime.sleep_ms(freq)
    nonsensical = [r for r in readings if r < 1]

    print("{pct:0.0%} nonsensical readings at frequency {freq}ms ({count} nonsensical readings in {samples} samples. readings:{readings}".format(
        pct=len(nonsensical) / samples, freq=freq, count=len(nonsensical), samples=samples, readings=readings))
