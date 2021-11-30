# micropython-motor-driver-dual-tb6612fng

A MicroPython driver for [SparkFun Motor Driver - Dual TB6612FNG boards](https://www.sparkfun.com/products/14450) that use the Toshiba TB6612FNG IC. There is support for one or two ICs.

Lets you control either or both DC motors via SparkFun Motor Driver Dual TB6612FNG boards.

## Usage

```py
from tb6612fng import Motors, Motor
import utime

# Provide GPIO Pin IDs that MicroPython's machine.Pin class recognizes
motor_a_pin1 = 14
motor_a_pin2 = 15
motor_a_pwm  = 13

motor_b_pin1 = 16
motor_b_pin2 = 17
motor_b_pwm  = 18

stby_pin = 10

# Setup each motor in a dual motor controller:
left = Motor(motor_a_pin1, motor_a_pin2, motor_a_pwm)
right = Motor(motor_b_pin1, motor_b_pin2, motor_b_pwm)
# Control both motors at once:
motors = Motors(left, right, stby_pin)

motors.forward()
utime.sleep(2)

motors.stop()
utime.sleep(2)

motors.reverse()
utime.sleep(2)

motors.spin_left()
utime.sleep(2)

motors.spin_right()
utime.sleep(2)

motors.disable()
```

## Notes & References

Using [SparkFun Motor Driver - Dual TB6612FNG](https://www.sparkfun.com/products/14450) with a Raspberry Pi Pico RP2040 & MicroPython.

Hardware hookup guide is at https://learn.sparkfun.com/tutorials/tb6612fng-hookup-guide

Since we're using a Raspberry Pi Pico instead of Arduino, [Sparkfun's Arduino driver](https://github.com/sparkfun/SparkFun_TB6612FNG_Arduino_Library) doesn't work.
