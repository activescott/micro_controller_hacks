# Serial (I2C) driver for SparkFun OpenLCD https://github.com/sparkfun/OpenLCD
# references for command ids etc at https://github.com/sparkfun/SparkFun_SerLCD_Arduino_Library
import machine
import utime


SETTING_COMMAND = const(0x7C)
SPECIAL_COMMAND = const(254)
CLEAR_COMMAND = const(0x2D)
SET_RGB_COMMAND = const(0x2B)
# Special Commands:
LCD_SETDDRAMADDR = const(0x80)
LCD_DISPLAYCONTROL = const(0x08)
# on/off states:
LCD_DISPLAYON = const(0x04)
LCD_DISPLAYOFF = const(0x00)
LCD_CURSORON = const(0x02)
LCD_CURSOROFF = const(0x00)
LCD_BLINKON = const(0x01)
LCD_BLINKOFF = const(0x00)


# TODO: OpenLCD is more of a driver. Needs moved to drivers.
class OpenLCD:
    def __init__(self, sda_pin, scl_pin, i2c_bus, i2c_periphial_id, max_rows=2, max_columns=16):
        sda = machine.Pin(sda_pin)
        scl = machine.Pin(scl_pin)
        self.i2c = machine.I2C(i2c_bus, sda=sda, scl=scl, freq=400000)
        self.i2c_periphial_id = i2c_periphial_id
        self.max_rows = max_rows
        self.max_columns = max_columns
        # I2C buses in these devices seem to need time to recover: https://forum.micropython.org/viewtopic.php?t=4746
        utime.sleep_ms(10)
        # default states:
        self._display_control_state = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF

    def deinit(self):
        # if self.i2c is not None:
        #    # only on WiPy?! self.i2c.deinit()
        #    self.i2c = None
        pass

    def __enter__(self):
        pass

    def __exit__(self):
        self.deinit()

    def scan(self):
        return self.i2c.scan()

    def _write(self, msg):
        self.i2c.writeto(self.i2c_periphial_id, msg)

    def command(self, cmd: int, other_data: bytearray=None):
        bits = bytearray([SETTING_COMMAND, cmd])
        if other_data is not None:
            bits = bits + other_data
        self._write(bits)
        # time to process it
        utime.sleep_ms(10)

    def command_special(self, cmd):
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
            raise ValueError(
                "invalid row. Rows expected to be less than {}.".format(len(row_offsets) - 1))
        val = LCD_SETDDRAMADDR | (col + row_offsets[row])
        self.command_special(val)

    def write(self, text):
        """
        Writes the specified text to the screen at the current location.
        """
        self._write(text)

    def on(self):
        """Turn display on"""
        self._display_control_state |= LCD_DISPLAYON
        self.command_special(self._display_control_state | self._display_control_state)

    def off(self):
        """Turn display off"""
        self._display_control_state &= ~LCD_DISPLAYON
        self.command_special(self._display_control_state | self._display_control_state)

    def color(self, red=0xFF, green=0xFF, blue=0xFF):
        # keep the range of these in 0-0xFF
        def limit(val: int) -> int:
            val = max(0, val)
            val = min(0xFF, val)
            return val
        red = limit(red)
        green = limit(green)
        blue = limit(blue)
        # each 1-byte color component is actually encoded in the range of 0-29:
        def encode(val: int) -> int:
            return round(val / 0xFF * 29.0)
        self.command(SET_RGB_COMMAND, bytearray([encode(red), encode(green), encode(blue)]))
        
