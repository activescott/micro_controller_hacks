# testing two SPI devices: An LCD and a Compass:
import utime
from qmc5883l import Compass
#from open_lcd import OpenLCD
from constants import COMPASS_I2C_SDA_PIN, COMPASS_I2C_SCL_PIN, COMPASS_I2C_BUS, LCD_PIN_SDA, LCD_PIN_SCL, LCD_I2C_BUS, LCD_I2C_PERIPH_ID

#lcd = OpenLCD(LCD_PIN_SDA, LCD_PIN_SCL, LCD_I2C_BUS, LCD_I2C_PERIPH_ID)
comp = Compass(COMPASS_I2C_SDA_PIN, COMPASS_I2C_SCL_PIN, COMPASS_I2C_BUS)
comp.init(Compass.MODE_CONTINUOUS)

for cnt in range(10):
    #reading = comp.read_smooth()
    reading = comp.read()
    msg = "test {} head: {}".format(cnt, reading["heading"])
    print(msg)
    #lcd.clear()
    #lcd.write(msg)
    utime.sleep(1)
