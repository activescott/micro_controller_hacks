# Getting Started with MicroPython on Raspberry Pi Pico, Chapter 4...
# Inputs: reading a button
import machine, utime

button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
led_onboard = machine.Pin(25, machine.Pin.OUT)

print("Button: {}".format(button.value()))

push_count = 0

while True:
    led_onboard.value(0)
    if button.value() == 1:
        led_onboard.value(1)
        push_count = push_count + 1
        print("Button pushed {} times!".format(push_count))
        utime.sleep(0.1)
