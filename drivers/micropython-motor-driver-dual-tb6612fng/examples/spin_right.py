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
    print("spin right")
    motors.spin_right(speed=SPEED_MAX * 0.5)
    MS_PER_SECOND = 1000.0
    utime.sleep_ms(round(MS_PER_SECOND * 0.25))

    print("stop_hard")
    motors.stop_hard()
    utime.sleep(2)
    
finally:
    # try/finally so that if things went wrong disable the motor driver and don't leave motors running
    print("disable")
    motors.disable()
