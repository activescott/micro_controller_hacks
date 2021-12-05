# micropython-qmc5883l-magnetic-compass-sensor-driver

MicroPython driver for the QMC5883L 3-Axis Magnetic, Digital Compass IC from QST Corporation (often sold as a HMC5883L as described at https://surtrtech.com/2018/02/01/interfacing-hmc8553l-qmc5883-digital-compass-with-arduino/).

## Usage

```py
import utime
from constants import I2C_SDA_PIN, I2C_SCL_PIN, COMPASS_I2C_BUS
from qmc5883l import Compass

comp = Compass(I2C_SDA_PIN, I2C_SCL_PIN, COMPASS_I2C_BUS)

for count in range(10**3):
    reading = comp.read_smooth()
    print("{direction:>2}, heading: {heading:>6} x:{x:>8} y:{y:>8} z:{z:>8}".format(
        **reading))
    utime.sleep(0.2)
    count -= 1

```
