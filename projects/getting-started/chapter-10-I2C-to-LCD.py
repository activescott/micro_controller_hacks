# Getting Started with MicroPython on Raspberry Pi Pico, Chapter 10...
# I2C to LCD
import machine
import utime

utime.sleep(2)

sda = machine.Pin(0)
scl = machine.Pin(1)

i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)
i2c.writeto(114, '\x7c')
i2c.writeto(114, '\x2D')
i2c.writeto(114, 'Hello world!')

print("I2C scan device list: {}".format(i2c.scan()))