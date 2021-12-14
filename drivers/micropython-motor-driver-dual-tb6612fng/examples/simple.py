# my "hello world" of motors
import utime
from tb6612fng import Motors, Motor, SPEED_MAX
from constants import MOTOR_STBY_PIN, MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM, MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM

print("initializing left/right")
left = Motor(MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM)
right = Motor(MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM)

print("initializing motors")
motors = Motors(left, right, MOTOR_STBY_PIN)

try:
    speed = SPEED_MAX / 4
    print("forward @ {}...".format(speed))
    motors.forward(speed)

    utime.sleep(2)

    print("stop")
    motors.stop()
    utime.sleep(2)

    print("reverse")
    motors.reverse()
    utime.sleep(2)

    print("stop_hard")
    motors.stop_hard()
    utime.sleep(2)

    print("spin left")
    motors.spin_left()
    utime.sleep(2)

    print("spin right")
    motors.spin_right()
    utime.sleep(2)

finally:
    # try/finally so that if things went wrong disable the motor driver and don't leave motors running
    print("disable")
    motors.disable()
