
# So... it turns out my chip is a QMC5883 instead or a "fake hmc8553l" as explained at https://surtrtech.com/2018/02/01/interfacing-hmc8553l-qmc5883-digital-compass-with-arduino/
# So I never finished this driver, but it is probably approximately close as I read the datasheet carefully and repeatedly was trying to make this thing work when I deided I check the ID on the chip.

# MicroPython driver to read Honeywell HMC5883L 3-Axis Magnetic Electronic Compass Module
# References:
# - Honeywell Datasheet: https://cdn-shop.adafruit.com/datasheets/HMC5883L_3-Axis_Digital_Compass_IC.pdf
# - sunfounder.cc wiki: http://wiki.sunfounder.cc/index.php?title=GY-271_HMC5883L_3-Axis_Magnetic_Electronic_Compass_Module
import machine
import utime

# from datasheet:
I2C_READ_ADDRESS = const(0x3D)
I2C_WRITE_ADDRESS = const(0x3C)    
# Info from datasheet on reading/writing to device:
# The devices uses an address pointer to indicate which register location is to be read from or written to.
# These pointer locations are sent from the master to this slave device and succeed the 7-bit address (0x1E) plus 1 bit read/write identifier, i.e. 0x3D for read and 0x3C for write.
# ... For example, to move the address pointer to register 10, send 0x3C 0x0A.
# Register Addresses (from page 11 of data sheet):
# Data Output X LSB Register Read Data Output Z MSB Register Read Data Output Z LSB Register Read Data Output Y MSB Register Read Data Output Y LSB Register Read Status Register Read Identification Register A Read Identification Register B Read Identification Register C Read
# Address Location  Name                        Access
# 00                Configuration Register A    Read/Write
# 01                Configuration Register B    Read/Write   
# 02                Mode Register               Read/Write
MODE_REGISTER = const(0x02)
# 03                Data Output X MSB Register  Read
# 04                Data Output X LSB Register  Read
# 05                Data Output Z MSB Register  Read
# 06                Data Output Z LSB Register  Read
# 07                Data Output Y MSB Register  Read
# 08                Data Output Y LSB Register  Read
# 09                Status Register             Read
STATUS_REGISTER = const(0x09)
# 10                Identification Register A   Read
IDENTIFICATION_REGISTER_A = const(0xA)
# 11                Identification Register B   Read
IDENTIFICATION_REGISTER_B = const(0xB)
# 12                Identification Register C   Read
IDENTIFICATION_REGISTER_C = const(0xC)

# 400 kHZ frequency/rate from datasheet is max.
I2C_RATE = const(400000)
        
class Compass:
    """
    Provides methods to read a Honeywell HMC5883L 3-Axis Magnetic, Digital Compass IC.
    """
    def __init__(self, sda_pin_id, scl_pin_id, i2c_id=0, i2c_bus_address=0x0D):
        """
        Initializes a new compass reader.

        - `sda_pin_id`: Pin ID identifying the pin for the I2C SDA pin.
        - `scl_pin_id`: Pin ID identifying the pin for the I2C SCL pin.
        - `i2c_id`: Identifies a particular I2C peripheral. Allowed values for depend on the particular port/board
        """
        sda = machine.Pin(sda_pin_id)
        scl = machine.Pin(scl_pin_id)
        self.i2c = machine.I2C(i2c_id, sda=sda, scl=scl, freq=I2C_RATE)
        self.i2c_bus_address = i2c_bus_address
    
    def scan(self):
        return self.i2c.scan()
    
    def status(self):
        """
        Returns a value that indicates device status
        """
        acks = self.i2c.writeto(self.i2c_bus_address, bytes([I2C_READ_ADDRESS, STATUS_REGISTER]))
        acks = self.i2c.writeto(self.i2c_bus_address, bytes([STATUS_REGISTER]))
        utime.sleep(0.5)
        bits = self.i2c.readfrom(self.i2c_bus_address, 1)
        print("bits:" + str(bits))
        #LOCK = bits[0] & 0x02
        #RDY = bits[0] & 0x01
        #print("(LOCK, RDY)" + str((LOCK, RDY)))
        return bits[0]
    
    
        
        