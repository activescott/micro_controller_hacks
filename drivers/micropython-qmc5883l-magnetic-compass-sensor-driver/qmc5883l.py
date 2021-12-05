# MicroPython driver for the QMC5883L 3-Axis Magnetic, Digital Compass IC from QST Corporation (often sold as a HMC5883L as described at https://surtrtech.com/2018/02/01/interfacing-hmc8553l-qmc5883-digital-compass-with-arduino/).
import machine
import utime
import math
import struct

REGISTER_MEASUREMENT_DATA = const(0x00)
REGISTER_STATUS = const(0x06)
REGISTER_CONTROL = const(0x09)
REGISTER_RESET_PERIOD = const(0x0B)
REGISTER_RESERVED_IDC = const(0x20)
REGISTER_RESERVED_IDD = const(0x21)


def direction(heading):
    """Returns N NE E SE S SW or W from the specified heading."""
    # Create the eight named directions in order of their 360deg heading:
    directions = [
        "N",  # 0°
        "NE",  # 45°
        "E",  # 90°
        "SE",  # 135°
        "S",  # 180°
        "SW",  # 225°
        "W",  # 270°
        "NW",  # 315°
        "N"  # 360°
    ]
    # convert and round heading off to 1 of 8 headings (well 9  because we make both 0 & 360 N):
    l = len(directions)
    index = round((heading / 360.0) * l - 1)
    # handle <0 & >8
    index = max(0, min(l-1, index))
    return directions[index]


class Compass:
    """
    Provides methods to read a QMC5883L 3-Axis Magnetic, Digital Compass IC from QST Corporation.
    """

    # Modes:
    MODE_CONTINUOUS = const(0b01)
    MODE_STANDBY = const(0b00)

    # Output Data Rates (ODR):
    # For most of compassing applications, we recommend 10 Hz for low power consumption.
    # For gaming, the high update rate such as 100Hz or 200Hz can be used.
    OUTPUT_DATA_RATE_10HZ = const(0b0000)
    OUTPUT_DATA_RATE_50HZ = const(0b0100)
    OUTPUT_DATA_RATE_100HZ = const(0b1000)
    OUTPUT_DATA_RATE_200HZ = const(0b1100)

    # Field Ranges (RNG):
    # The full scale field range is determined by the application environments.
    # For magnetic clear environment, low field range such as +/- 2gauss can be used.
    # The field range goes hand in hand with the sensitivity of the magnetic sensor.
    # The lowest field range has the highest sensitivity, therefore, higher resolution.
    RNG_2G = const(0b000000)
    RNG_8G = const(0b010000)

    # Over Sample Ratio (OSR):
    #  Larger OSR value leads to smaller filter bandwidth, less in-band noise and higher power consumption
    OSR_512 = const(0b00000000)
    OSR_256 = const(0b0100000000)
    OSR_128 = const(0b1000000000)
    OSR_064 = const(0b1100000000)

    def __init__(self, sda_pin_id, scl_pin_id, i2c_id=0, declination=0, i2c_bus_address=0x0D):
        """
        Initializes a new compass reader.

        - `sda_pin_id`: Pin ID identifying the pin for the I2C SDA pin.
        - `scl_pin_id`: Pin ID identifying the pin for the I2C SCL pin.
        - `i2c_id`: Identifies a particular I2C peripheral. Allowed values for depend on the particular port/board
        - `declination`: For more about declanation see http://www.compassdude.com/compass-declination.php
        """
        sda = machine.Pin(sda_pin_id)
        scl = machine.Pin(scl_pin_id)
        # 400 kHZ frequency/rate from datasheet is max.
        I2C_RATE = const(400000)
        self.i2c = machine.I2C(i2c_id, sda=sda, scl=scl, freq=I2C_RATE)
        self.i2c_bus_address = i2c_bus_address
        self.declination = declination
        self.init(Compass.MODE_CONTINUOUS)

    def init(self, mode, data_rate=OUTPUT_DATA_RATE_200HZ, field_range=RNG_2G, sample_ratio=OSR_512):
        """
        Initializes the device.
        - `mode` must be one of: `Compass.MODE_CONTINUOUS` or `Compass.MODE_STANDBY`
        - `data_rate` must be one of: `Compass.OUTPUT_DATA_RATE_10HZ`, Compass.OUTPUT_DATA_RATE_50HZ`, `Compass.OUTPUT_DATA_RATE_100HZ`, or `Compass.OUTPUT_DATA_RATE_200HZ`
        - `field_range` must be one of `Compass.RNG_2G`, or `Compass.RNG_8G`.
        - `sample_ratio` must be one of `Compass.OSR_512`, or `Compass.OSR_256`, `Compass.OSR_128`, or `Compass.OSR_064`.        
        """
        # SET/RESET Period is controlled by FBR [7:0], it is recommended that the register 0BH is written by 0x01.

        self.i2c.writeto(self.i2c_bus_address, bytes(
            [REGISTER_RESET_PERIOD, 0x01]))
        # Write Register 09H by 0x1D (Define OSR = 512, Full Scale Range = 8 Gauss, ODR = 200Hz, set continuous measurement mode)
        value = mode | data_rate | field_range | sample_ratio
        self.i2c.writeto(self.i2c_bus_address,
                         bytes([REGISTER_CONTROL, value]))

    def status(self):
        """
        Returns a tuple containing `(DATA_READY, OVERFLOW, DATA_SKIP)`
        Values for each are:
        - DATA_READY: False: no new data, True: new data is ready
        - OVERFLOW: True if any data of three axis magnetic sensor channels is out of range.
        - DATA_SKIP: Data Skip (DOR) bit is set to “1” if all the channels of output data registers are skipped in reading in the continuous-measurement mode.
        """
        self.i2c.writeto(self.i2c_bus_address, bytes([REGISTER_STATUS, 0x01]))
        bits = self.i2c.readfrom(self.i2c_bus_address, 1)
        print("Status:" + str(bits))
        DATA_READY = 0b0001
        OVERFLOW = 0b0010
        DATA_SKIP = 0b0100
        return {
            "DATA_READY": bits[0] & DATA_READY == DATA_READY,
            "OVERFLOW": bits[0] & OVERFLOW == OVERFLOW,
            "DATA_SKIP": bits[0] & DATA_SKIP == DATA_SKIP
        }

    def read_smooth(self, samples=10):
        """Returns measurement data after smoothing it out"""
        # read it samples times and throw out the highest and lowest readings:
        x = 0
        y = 0
        z = 0
        heading = 0
        counter = samples
        while counter > 0:
            read = self.read()
            x += read['x']
            y += read['y']
            z += read['z']
            heading += read['heading']
            counter -= 1
        x = x / samples
        y = y / samples
        z = z / samples
        heading = heading / samples
        return dict(x=x, y=y, z=z, heading=heading, direction=direction(heading))

    def read(self):
        """
        Returns the measurement data
        """
        # Registers 00H ~ 05H store the measurement data from each axis magnetic sensor in continuous-measurement.
        self.i2c.writeto(self.i2c_bus_address, bytes(
            [REGISTER_MEASUREMENT_DATA]))
        bits = self.i2c.readfrom(self.i2c_bus_address, 6)
        # there are three 16 bit **signed** ints here. In python `x = bits[0] | (bits[1] << 8)` returned unsigned ints without any clear way to convert them but struct.unpack can deal with it:
        x = struct.unpack('h', bits[0:2])[0]
        y = struct.unpack('h', bits[2:4])[0]
        z = struct.unpack('h', bits[4:6])[0]

        # The calculation of atan gives raidans. More detail on this at:
        # - https://en.wikipedia.org/wiki/Radian
        # - http://www.compassdude.com/compass-declination.php
        DEGREES_PER_RADIAN = 57.29578  # 180 / PI
        heading = math.atan2(x, y) * DEGREES_PER_RADIAN
        if heading < 0:
            heading += 360
        heading = 360 - heading  # N=0/360, E=90, S=180, W=270
        heading = heading + self.declination

        return dict(heading=heading, x=x, y=y, z=z, direction=direction(heading))

    def scan(self):
        return self.i2c.scan()
