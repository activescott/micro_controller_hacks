# Getting Started with MicroPython on Raspberry Pi Pico, Chapter 8...
# Temperature Gauge
import machine
import utime

# ADC Channel 4 is built-in temp sensor
sensor_temperature = machine.ADC(4)

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
    print("Temperature is {}f.".format(fahrenheight))
    utime.sleep(1)
    
