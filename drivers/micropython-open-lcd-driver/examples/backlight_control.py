import utime
from constants import LCD_PIN_SDA, LCD_PIN_SCL, LCD_I2C_BUS, LCD_I2C_PERIPH_ID
from open_lcd import OpenLCD

lcd = OpenLCD(LCD_PIN_SDA, LCD_PIN_SCL,
              LCD_I2C_BUS, LCD_I2C_PERIPH_ID, max_rows=2, max_columns=16)


""" lcd.clear()

lcd.backlight_off()
lcd.clear()
lcd.write("backlight is off")

utime.sleep(2)

lcd.backlight_on()
lcd.clear()
lcd.write("backlight is on")
 """

lcd.on()

for seconds in range(3, 0, -1):
  lcd.clear()
  lcd.write("turning display off in {}...".format(seconds))
  utime.sleep(1)

lcd.off()
utime.sleep(2)

lcd.on()
lcd.clear()
lcd.write("display is back on!")
