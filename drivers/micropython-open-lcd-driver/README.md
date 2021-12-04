# micropython-open-lcd-driver

A MicroPython driver for [SparkFun OpenLCD-firmware LCD displays](https://github.com/sparkfun/OpenLCD) such as the [SparkFun 16x2 SerLCD - RGB Backlight](https://www.sparkfun.com/products/16396).

Uses I2C Serial (open to contributions ot support others).

## Usage

```py
import utime
from constants import LCD_PIN_SDA, LCD_PIN_SCL, LCD_I2C_BUS, LCD_I2C_PERIPH_ID
from open_lcd import OpenLCD

lcd = OpenLCD(LCD_PIN_SDA, LCD_PIN_SCL,
              LCD_I2C_BUS, LCD_I2C_PERIPH_ID, max_rows=2, max_columns=16)
lcd.clear()

msg = "row R col C"
for row in range(lcd.max_rows):
    for col in range(lcd.max_columns - len(msg) + 1):
        lcd.clear()
        lcd.move(row, col)
        lcd.write(msg.replace("R", str(row)).replace("C", str(col)))
        utime.sleep(1)
```

## Notes & References

- Supports the SparkFun OpenLCD firmware https://github.com/sparkfun/OpenLCD
- References for command IDs primarily from the Arduino I2C driver at https://github.com/sparkfun/SparkFun_SerLCD_Arduino_Library
- Tested with the [SparkFun 16x2 SerLCD - RGB Backlight](https://www.sparkfun.com/products/16396)
