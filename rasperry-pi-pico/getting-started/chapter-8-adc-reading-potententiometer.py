# Getting Started with MicroPython on Raspberry Pi Pico, Chapter 8...
# ADC - Reading Potententiometer
import machine
import utime
import math

pot = machine.ADC(26)
led = machine.PWM(machine.Pin(15))
led.freq(1000)

max_int = 2**16 - 1
to_volts_factor = 3.3 / max_int

last_reading = 0
while True:
    reading = pot.read_u16()
    led.duty_u16(reading)
    voltage = round(reading * to_volts_factor, 1)
    pct =  round(voltage / 3.3 * 100) 
    if pct != last_reading:
        print("Potententiometer is {: >3}% ({} volts, {} raw).".format(pct, voltage, reading))
        last_reading = pct
        utime.sleep(0.2)
