from tb6612fng import Motors, Motor, SPEED_MAX
import utime
from constants import MS_PER_SECOND, MOTOR_STBY_PIN, MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM, MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM

motors = None


def init():
    global motors
    print("initializing left/right")
    left = Motor(MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM)
    right = Motor(MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM)
    print("initializing motors")
    motors = Motors(left, right, MOTOR_STBY_PIN)


def disable():
    motors.disable()


def deinit():
    disable()


def stop():
    motors.stop_hard()
    # lets not leave the motors in the hard stopped state for long:
    utime.sleep_ms(int(MS_PER_SECOND * 0.25))
    motors.stop()


def forward():
    speed = SPEED_MAX / 2
    motors.forward()


def rotate_left_slightly():
    # numbers here purely trial & error.
    # spin a specified number of degrees according to compass
    motors.spin_right(speed=SPEED_MAX * 0.5)
    utime.sleep_ms(round(MS_PER_SECOND * 0.25))
    motors.stop_hard()
    utime.sleep_ms(int(MS_PER_SECOND * 0.1))
