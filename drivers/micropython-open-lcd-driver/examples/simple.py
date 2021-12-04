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
