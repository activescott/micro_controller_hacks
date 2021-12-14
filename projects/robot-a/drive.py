from tb6612fng import Motors, Motor, SPEED_MAX
import utime
from constants import MS_PER_SECOND, MOTOR_STBY_PIN, MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM, MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM
from constants import WHEEL_ENCODER_PIN_RIGHT, WHEEL_ENCODER_PIN_LEFT
from encoder import Encoder

motors = None
encoder_left = None
encoder_right = None


def init():
    global motors, encoder_left, encoder_right
    print("initializing left/right")
    left = Motor(MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM)
    right = Motor(MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM)
    print("initializing motors")
    motors = Motors(left, right, MOTOR_STBY_PIN)
    print("initializing encoders...")
    _HITS_PER_WHEEL_ROTATION = const(4)
    encoder_left = Encoder(WHEEL_ENCODER_PIN_LEFT,
                           hits_per_rotation=_HITS_PER_WHEEL_ROTATION)
    encoder_right = Encoder(WHEEL_ENCODER_PIN_RIGHT,
                            hits_per_rotation=_HITS_PER_WHEEL_ROTATION)


def disable():
    global motors
    if motors is not None:
        motors.disable()
        motors = None


def deinit():
    disable()


def stop():
    motors.stop_hard()
    # lets not leave the motors in the hard stopped state for long:
    utime.sleep_ms(int(MS_PER_SECOND * 0.25))
    motors.stop()


def default_speed():
    return SPEED_MAX / 4


def forward():
    motors.forward(default_speed())


def reverse():
    motors.reverse(default_speed())


def rotate_left_slightly():
    # numbers here purely trial & error.
    # spin a specified number of degrees according to compass
    motors.spin_left(speed=SPEED_MAX / 2)
    utime.sleep_ms(round(MS_PER_SECOND * 0.7))
    motors.stop_hard()
    utime.sleep_ms(int(MS_PER_SECOND * 0.1))


def left_speed() -> bool:
    return encoder_left.speed()


def right_speed() -> bool:
    return encoder_right.speed()


def left_stopped() -> bool:
    return encoder_left.speed() == 0


def right_stopped() -> bool:
    return encoder_left.speed() == 0
