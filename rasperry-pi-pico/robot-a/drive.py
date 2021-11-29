from tb6612fng import Motors, Motor, SPEED_MAX
import utime
from constants import MS_PER_SECOND

motors = None


def setup():
    global motors
    motor_a_pin1 = 14
    motor_a_pin2 = 15
    motor_a_pwm = 13

    motor_b_pin1 = 16
    motor_b_pin2 = 17
    motor_b_pwm = 18
    stby_pin = 10

    print("initializing left/right")
    left = Motor(motor_a_pin1, motor_a_pin2, motor_a_pwm)
    right = Motor(motor_b_pin1, motor_b_pin2, motor_b_pwm)
    print("initializing motors")
    motors = Motors(left, right, stby_pin)


def stop():
    # if we just do a normal stop, he doesn't stop fast enough and keeps rolling forward too long. So we do a quick reverse to rapidly stop him:
    motors.reverse()
    utime.sleep_ms(round(MS_PER_SECOND * 0.01))
    motors.stop()


def forward():
    speed = SPEED_MAX / 2
    motors.forward()
