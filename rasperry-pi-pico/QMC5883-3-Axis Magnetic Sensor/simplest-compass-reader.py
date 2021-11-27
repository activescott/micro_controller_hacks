from qmc5883l import Compass
import utime

I2C_SDA_PIN = 0
I2C_SCL_PIN = 1


declination = 0#15 + (25/60)
comp = Compass(I2C_SDA_PIN, I2C_SCL_PIN, declination=declination)

devices = comp.scan()
print("Devices: {}".format(devices))

#status = comp.status()
#print("status:" + str(status))

#detected = comp.is_device_detected()
#print("detected:" + str(detected))

#comp.reset()

print("status:" + str(comp.status()))

print("init continuous")
comp.init(Compass.MODE_CONTINUOUS)
print("status:" + str(comp.status()))

count = 10**3
while count > 0:
    #reading = comp.read()
    reading = comp.read_smooth()
    #print("read:" + str(reading))
    print("{direction:>2}, heading: {heading:>6} x:{x:>8} y:{y:>8} z:{z:>8}".format(**reading))
    utime.sleep(0.2)
    count-=1

print("init standby")
comp.init(Compass.MODE_STANDBY, Compass.OUTPUT_DATA_RATE_200HZ, Compass.RNG_2G)
print("status:" + str(comp.status()))

