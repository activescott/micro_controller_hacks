# The simplest example of the HC-SR04 ultrasonic sensor working.
from hcsr04 import HCSR04
import utime

TRIGGER_PIN = 2
ECHO_PIN = 3

sensor = HCSR04(trigger_pin=TRIGGER_PIN, echo_pin=ECHO_PIN)

def log(msg):
  tt = utime.localtime()[3:6]
  prefix = "{:02d}:{:02d}.{:02d} ".format(*tt)
  print(prefix + msg)  


counter = 10**4
while counter > 0:
  counter -= 1
  utime.sleep(0.5)
  distance = sensor.distance_cm()  
  log("{} cm".format(distance))
