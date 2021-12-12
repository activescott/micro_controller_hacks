import uasyncio
from constants import WHEEL_ENCODER_PIN_LEFT
from constants import MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM, MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM, MOTOR_STBY_PIN
from encoder import Encoder
from tb6612fng import Motor, Motors, SPEED_MAX


def init_motors():
    global motors
    print("initializing left/right")
    left = Motor(MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM)
    right = Motor(MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM)
    print("initializing motors")
    return Motors(left, right, MOTOR_STBY_PIN)


async def main():
    # setup
    motors = init_motors()
    print("setting up encoder")
    with Encoder(WHEEL_ENCODER_PIN_LEFT) as encoder:
        # start moving
        speed = SPEED_MAX / 4.0
        motors.forward(speed)

        # how many spins will we allow?
        HITS_PER_WHEEL_ROTATION = 4
        ROTATIONS = 2
        MAX_HITS = HITS_PER_WHEEL_ROTATION * ROTATIONS

        # stop moving as soon as we hit a certain number of spins/hits:
        print("Counting to {} rotations...".format(ROTATIONS))
        while encoder.hits() < MAX_HITS:
            await uasyncio.sleep_ms(5)
            pass

        # stop
        motors.stop_hard()
        motors.disable()

        print(encoder)

uasyncio.run(main())
