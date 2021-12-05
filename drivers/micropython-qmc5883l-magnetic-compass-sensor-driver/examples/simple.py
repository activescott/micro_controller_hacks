import utime
from constants import I2C_SDA_PIN, I2C_SCL_PIN, COMPASS_I2C_BUS
from qmc5883l import Compass

comp = Compass(I2C_SDA_PIN, I2C_SCL_PIN, COMPASS_I2C_BUS)

devices = comp.scan()
print("Devices: {}".format(devices))
print("status:" + str(comp.status()))
print("status:" + str(comp.status()))

for count in range(10**3):
    reading = comp.read_smooth()
    print("{direction:>2}, heading: {heading:>6} x:{x:>8} y:{y:>8} z:{z:>8}".format(
        **reading))
    utime.sleep(0.2)
    count -= 1
