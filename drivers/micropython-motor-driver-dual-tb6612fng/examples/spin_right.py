# my "hello world" of motors
from tb6612fng import Motors, Motor, SPEED_MAX
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
