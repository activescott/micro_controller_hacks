import machine
import utime
from qmc5883l import Compass
from constants import COMPASS_I2C_SDA_PIN, COMPASS_I2C_SCL_PIN, COMPASS_I2C_BUS
from logger import Logger, WARNING, DEBUG
comp: Compass = None

log: Logger = None


def init(logger=Logger(level=DEBUG)):
    global comp, log
    comp = Compass(COMPASS_I2C_SDA_PIN, COMPASS_I2C_SCL_PIN, COMPASS_I2C_BUS)
    log = logger


def deinit():
    global comp
    if comp is not None:
        comp = None


def heading() -> float:
    try:
        reading = comp.read_smooth()
        log.debug("compas reading:" + str(reading))
        return reading["heading"]
    except OSError as ose:
        # have seen these "OSError: [Errno 5] EIO" periodically and intermittently
        log.error("OSError reading compass: {}".format(ose))
