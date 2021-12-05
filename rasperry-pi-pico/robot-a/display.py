import machine
import utime
from constants import LCD_PIN_SDA, LCD_PIN_SCL, LCD_I2C_BUS, LCD_I2C_PERIPH_ID
from open_lcd import OpenLCD

"""Module handles the "display" device for the robot."""


def _ensure_str(arg: str, max_len) -> str:
    if (arg is None) or (not isinstance(arg, str)):
        return ""
    return arg[0:max_len]


lcd: OpenLCD = None
_activity: str = ""
_distance: float = 0
_heading: float = 0


def init():
    global lcd
    lcd = OpenLCD(LCD_PIN_SDA, LCD_PIN_SCL,
                  LCD_I2C_BUS, LCD_I2C_PERIPH_ID)
    lcd.clear()


def deinit():
    global lcd
    if lcd is not None:
        lcd.deinit()
        lcd = None


def ljust(s: str, width: int) -> str:
    l = len(s)
    if l > width:
        return s[:width]
    elif l < width:
        return s + (" " * (width - l))
    else:
        return s


def _show(text: str, row: int) -> None:
    if row < 0 or row > lcd.max_rows:
        raise ValueError(
            "display row must be between 0 and {}".format(lcd.max_rows))
    text = _ensure_str(text, lcd.max_columns)
    try:
        lcd.move(row, 0)
        lcd.write(ljust(text, lcd.max_columns))
    except Exception as err:
        print("ERROR! failed to write to lcd:" + str(err))


def show_all() -> None:
    _show(_activity, 0)
    _show("dst:{:>3} hd:{:>3}".format(round(_distance), round(_heading)), 1)


def update_activity(activity: str) -> None:
    global _activity
    PREFIX = "STATE_"
    if activity.startswith(PREFIX):
        activity = activity[len(PREFIX):]
    _activity = activity


def update_heading(heading: float) -> None:
    global _heading
    _heading = heading


def update_distance(distance: float) -> None:
    global _distance
    _distance = distance


def update(activity: str | None = None, heading: float | None = None, distance: float | None = None) -> None:
    if activity is not None:
        update_activity(activity)
    if heading is not None:
        update_heading(heading)
    if distance is not None:
        update_distance(distance)
    show_all()


if __name__ == "__main__":
    print("display.__main__ " * 20)
    import random
    init()

    def test_dislay():
        print("scan:" + str(lcd.scan()))
        update("test 1", random.random() * 360, random.random() * 100)
        utime.sleep(1)

        update("test 2", random.random() * 360, random.random() * 100)
        utime.sleep(1)

        update("test 3", random.random() * 360, random.random() * 100)
        utime.sleep(1)
    
    def test_compass():
        from qmc5883l import Compass
        from constants import COMPASS_I2C_SDA_PIN, COMPASS_I2C_SCL_PIN, COMPASS_I2C_BUS

        for cnt in range(10):
            comp = Compass(COMPASS_I2C_SDA_PIN, COMPASS_I2C_SCL_PIN, COMPASS_I2C_BUS)
            reading = comp.read_smooth()
            update("test {}".format(cnt), reading["heading"], random.random() * 100)
            utime.sleep(1)

    
    test_compass()
