import uasyncio
from constants import WHEEL_ENCODER_PIN_RIGHT
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
    with Encoder(WHEEL_ENCODER_PIN_RIGHT) as encoder:
        # start moving
        speed = SPEED_MAX / 4.0
        motors.forward(speed)

        while True:
            print("speed: {}".format(encoder.speed()))
            await uasyncio.sleep_ms(1000)

        # stop
        motors.stop_hard()
        motors.disable()

        print(encoder)
        

uasyncio.run(main())
