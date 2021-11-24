# Getting Started with MicroPython on Raspberry Pi Pico, Chapter 4...
# Hello, LED!
import machine
import utime
import random

led_onboard = machine.Pin(25, machine.Pin.OUT)
led_green = machine.Pin(0, machine.Pin.OUT)
led_red = machine.Pin(1, machine.Pin.OUT)


def rand_on_off():
    return random.randint(0, 1)


while True: 
  led_onboard.toggle()
  led_green.value(rand_on_off())
  led_red.value(rand_on_off())
  utime.sleep(0.1)
