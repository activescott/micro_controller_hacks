# my "hello world" of motors
from tb6612fng import Motors, Motor
import utime

motor_a_pin1 = 14
motor_a_pin2 = 15
motor_a_pwm  = 13

motor_b_pin1 = 16
motor_b_pin2 = 17
motor_b_pwm  = 18

stby_pin = 10

print("initializing left/right")
left = Motor(motor_a_pin1, motor_a_pin2, motor_a_pwm)
right = Motor(motor_b_pin1, motor_b_pin2, motor_b_pwm)

print("initializing motors")
motors = Motors(left, right, stby_pin)

try:
    print("forward...")
    motors.forward()

    utime.sleep(2)

    print("stop")
    motors.stop()
    utime.sleep(2)

    print("reverse")
    motors.reverse()

    utime.sleep(1)

    print("spin left")
    motors.spin_left()
    utime.sleep(1)

    print("spin right")
    motors.spin_right()
    utime.sleep(1)

finally:
    # try/finally so that if things went wrong disable the motor driver and don't leave motors running
    print("disable")
    motors.disable()
