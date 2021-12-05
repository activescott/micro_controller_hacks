# Getting Started with MicroPython on Raspberry Pi Pico, Chapter 10...
# I2C to LCD: Temp Sensor
import utime

utime.sleep(2)

## Setup LCD:
sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)

# ADC Channel 4 is built-in temp sensor
sensor_temperature = machine.ADC(4)

def display(message):
    i2c.writeto(114, '\x7c')
    i2c.writeto(114, '\x2D')
    i2c.writeto(114, message)


# setup a conversion factor for adc -> voltage
volts = 3.3
int_max = 2 ** 16 - 1
adc_to_voltage_factor = volts/int_max


# read sensor:
while True:
    reading = sensor_temperature.read_u16() * adc_to_voltage_factor
    # convert voltage to degrees Celsius. Constants from RP2040 datsheet:
    # "Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV per degree. Therefore the temperature can be approximated as follows:
    # "T = 27 - (ADC_voltage - 0.706)/0.001721"
    celsius = 27 - (reading - 0.706) / 0.001721
    fahrenheight = (celsius * 1.8) + 32
    # print("Temp is {}f.".format(fahrenheight))
    display("Temp is {}f.".format(fahrenheight))
    utime.sleep(1)
