import time, os

print("hello, pico! The time is {}.".format(time.localtime()))
print("I am running on a {} {}".format(os.uname().machine, os.uname()))
mhz = 1000000
print("My CPU frequency is {} mhz".format(machine.freq()/mhz))

      
