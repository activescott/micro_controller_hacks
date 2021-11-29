# Hello, LED! This blinks an LED built into the pico. No external hardware needed.
# Probably the simplest possible example of pico.
import machine
import utime
import random

led_onboard = machine.Pin(25, machine.Pin.OUT)

while True: 
  led_onboard.toggle()
  utime.sleep(0.1)
