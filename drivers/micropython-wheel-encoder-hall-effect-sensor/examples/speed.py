import uasyncio
from constants import WHEEL_ENCODER_PIN_RIGHT, WHEEL_ENCODER_PIN_LEFT
from constants import MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM, MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM, MOTOR_STBY_PIN
from encoder import Encoder
from tb6612fng import Motor, Motors, SPEED_MAX
import micropython


def init_motors():
    global motors
    print("initializing left/right")
    left = Motor(MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM)
    right = Motor(MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM)
    print("initializing motors")
    return Motors(left, right, MOTOR_STBY_PIN)


async def main():
    micropython.alloc_emergency_exception_buf(100)
    # setup
    motors = init_motors()
    print("setting up encoder")
    with Encoder(WHEEL_ENCODER_PIN_RIGHT) as encoder_right, Encoder(WHEEL_ENCODER_PIN_LEFT) as encoder_left:
        # start moving
        speed = SPEED_MAX / 4.0
        motors.forward(speed)

        while True:
            print("speed: {:.2f} {:.2f}".format(encoder_left.speed(), encoder_right.speed()))
            await uasyncio.sleep_ms(500)

        # stop
        motors.stop_hard()
        motors.disable()

        print(encoder)
        

uasyncio.run(main())
