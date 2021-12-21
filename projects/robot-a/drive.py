from tb6612fng import Motors, Motor, SPEED_MAX
import utime
from constants import MS_PER_SECOND, MOTOR_STBY_PIN, MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM, MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM
from constants import WHEEL_ENCODER_PIN_RIGHT, WHEEL_ENCODER_PIN_LEFT
from encoder import Encoder
from random import choice

motors = None
encoder_left = None
encoder_right = None
forward_started_at = -1


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
    global forward_started_at
    forward_started_at = -1
    motors.stop_hard()
    # lets not leave the motors in the hard stopped state for long:
    utime.sleep_ms(int(MS_PER_SECOND * 0.25))
    motors.stop()


def default_speed():
    return SPEED_MAX / 2


def forward():
    global forward_started_at
    if forward_started_at == -1:
        forward_started_at = utime.ticks_ms()
    motors.forward(default_speed())


def reverse():
    global forward_started_at
    forward_started_at = -1
    motors.reverse(default_speed())


DIRECTION_RANDOM = 0
DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2


def spin_slightly(direction=DIRECTION_RANDOM):
    """
    Spins left or right slightly. 
    Arguments:
    - direction: Use `DIRECTION_RANDOM`, `DIRECTION_LEFT` or `DIRECTION_RIGHT`.
    """
    global forward_started_at
    forward_started_at = -1
    # numbers here purely trial & error.
    # TODO: spin a specified number of degrees according to **compass**
    if direction == DIRECTION_RANDOM:
        # coin flip:
        direction = choice([DIRECTION_LEFT, DIRECTION_RIGHT])

    if direction == DIRECTION_LEFT:
        motors.spin_left(speed=SPEED_MAX / 2)
    elif direction == DIRECTION_RIGHT:
        motors.spin_right(speed=SPEED_MAX / 2)
    else:
        assert False, "invalid direction '{}'!".format(direction)

    utime.sleep_ms(round(MS_PER_SECOND * 0.7))
    motors.stop_hard()
    utime.sleep_ms(int(MS_PER_SECOND * 0.1))


def forward_duration_ms():
    global forward_started_at
    print("forward_started_at:", forward_started_at)
    if forward_started_at == -1:
        return 0
    now = utime.ticks_ms()
    return utime.ticks_diff(now, forward_started_at)


def left_speed() -> bool:
    return encoder_left.speed()


def right_speed() -> bool:
    return encoder_right.speed()


def left_stopped() -> bool:
    return left_speed() == 0


def right_stopped() -> bool:
    return right_speed() == 0
