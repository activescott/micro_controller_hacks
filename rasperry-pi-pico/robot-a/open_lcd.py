# Serial (I2C) driver for SparkFun OpenLCD https://github.com/sparkfun/OpenLCD
# references for command ids etc at https://github.com/sparkfun/SparkFun_SerLCD_Arduino_Library
import machine
import utime


SETTING_COMMAND = 0x7C
SPECIAL_COMMAND = 254
CLEAR_COMMAND = 0x2D
# Special Commands:
LCD_SETDDRAMADDR = 0x80



class OpenLCD:
    def __init__(self, sda_pin, scl_pin, i2c_bus, i2c_periphial_id, max_rows=2, max_columns=16):
        sda = machine.Pin(4)
        scl = machine.Pin(5)
        self.i2c = machine.I2C(i2c_bus, sda=sda, scl=scl, freq=400000)
        self.i2c_periphial_id = i2c_periphial_id
        self.max_rows = max_rows
        self.max_columns = max_columns

    def _write(self, msg):
        self.i2c.writeto(self.i2c_periphial_id, msg)
        

    def command(self, cmd):
        self._write(chr(SETTING_COMMAND))
        self._write(chr(cmd))
        # time to process it
        utime.sleep_ms(10)

    def command_special(self, cmd):
        #self._write(chr(SPECIAL_COMMAND))
        #self._write(chr(cmd))
        bits = bytearray([SPECIAL_COMMAND, cmd])
        self._write(bits)
        # special commands may take longer to process
        utime.sleep_ms(50)

    def clear(self, ):
        """
        Clear display and return cursor to the starting position.
        """
        self.command(CLEAR_COMMAND)

    def move(self, row, col):
        """
        Move the cursor to the specified row & column.
        """
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        row = min(row, self.max_rows - 1)
        if row > len(row_offsets) - 1:
            raise ValueError("invalid row. Rows expected to be less than {}.".format(len(row_offsets) - 1))
        val = LCD_SETDDRAMADDR | (col + row_offsets[row])
        print("val:{:x}".format(val))
        self.command_special(val)

    def write(self, text):
        """
        Writes the specified text to the screen at the current location.
        """
        self._write(text)
