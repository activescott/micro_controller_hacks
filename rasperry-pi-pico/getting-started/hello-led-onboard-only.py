# Getting Started with MicroPython on Raspberry Pi Pico, Chapter 4...
# Hello, LED!
import machine
import utime
import random

led_onboard = machine.Pin(25, machine.Pin.OUT)

while True: 
  led_onboard.toggle()
  utime.sleep(0.1)
