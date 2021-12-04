import utime
from constants import LCD_PIN_SDA, LCD_PIN_SCL, LCD_I2C_BUS, LCD_I2C_PERIPH_ID
from open_lcd import OpenLCD

lcd = OpenLCD(LCD_PIN_SDA, LCD_PIN_SCL,
              LCD_I2C_BUS, LCD_I2C_PERIPH_ID, max_rows=2, max_columns=16)

def wait():
  for seconds in range(3, 0, -1):
    lcd.write(" {}...".format(seconds))
    utime.sleep(1)

def basic_colors():
  lcd.on()

  lcd.clear()
  lcd.write("bright")
  lcd.color(red=0xFF, green=0xFF, blue=0xFF)
  wait()

  lcd.clear()
  lcd.write("red")
  lcd.color(red=0xFF, green=0x00, blue=0x00)
  wait()

  lcd.clear()
  lcd.write("green")
  lcd.color(red=0x00, green=0xFF, blue=0x00)

  wait()

  lcd.clear()
  lcd.write("blue")
  lcd.color(red=0x00, green=0x00, blue=0xFF)
  wait()

  lcd.clear()
  lcd.write("bright")
  lcd.color(red=0xFF, green=0xFF, blue=0xFF)
  wait()

  lcd.clear()

basic_colors()

def all_colors():
  step = 50
  for red in range(0, 255, step):
    for green in range(0, 255, step):
      for blue in range(0, 255, step):
        lcd.clear()
        lcd.write("r:{} g:{} b:{}".format(red, green, blue))
        lcd.color(red=red, green=red, blue=blue)
        utime.sleep_ms(100)
