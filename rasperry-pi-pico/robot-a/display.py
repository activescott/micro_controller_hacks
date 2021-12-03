import machine
import utime
from constants import LCD_PIN_SDA, LCD_PIN_SCL, LCD_I2C_BUS, LCD_I2C_PERIPH_ID


from open_lcd import OpenLCD

lcd = OpenLCD(LCD_PIN_SDA, LCD_PIN_SCL, LCD_I2C_BUS, LCD_I2C_PERIPH_ID)
lcd.clear()
#lcd.move(0,0)
lcd.write("hi row 1")
lcd.move(1,0)
lcd.write("hi row 2")

