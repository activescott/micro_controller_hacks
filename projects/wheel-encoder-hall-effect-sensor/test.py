# testing hall-effect sensor use as a wheel encoder to know how much a non-servo motor is spinning.
import utime
from utime import ticks_us, ticks_diff
from machine import Pin
from constants import WHEEL_ENCODER_PIN_LEFT, US_PER_SECOND
from constants import MOTOR_STBY_PIN, MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM, MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM
from tb6612fng import Motors, Motor, SPEED_MAX
from array import array
from collections import deque

#ticks = array("i", [-1] * 3)
#MAX_TICK = len(ticks) - 1
#next_tick = 0
ticks = deque(tuple(), 10)
for i in range(10):
    ticks.append(0)

def encoder_callback(pin):
    #global ticks, next_tick
    #ticks[next_tick] = ticks_us()
    #next_tick = next_tick + 1 if next_tick < MAX_TICK - 1 else 0
    tick = ticks_us()
    ticks.append(tick)
    print(tick)


# we're going to run a motor at a low speed and look for indicators from the hall effect sensor to detect motor spinning.
encoder = Pin(WHEEL_ENCODER_PIN_LEFT, Pin.OPEN_DRAIN)
encoder.irq(encoder_callback)

print("initializing left/right")
left = Motor(MOTOR_A_PIN1, MOTOR_A_PIN2, MOTOR_A_PWM)
right = Motor(MOTOR_B_PIN1, MOTOR_B_PIN2, MOTOR_B_PWM)
print("initializing motors")
motors = Motors(left, right, MOTOR_STBY_PIN)

#####
motors.forward(SPEED_MAX)
for seconds in range(3, 0, -1):
    print("waiting {} seconds...".format(seconds))
    utime.sleep_ms(1000)

motors.disable()

queue = ticks
ticks = []
while len(queue) > 0:
    ticks.append(queue.popleft())
print("ticks:" + str(ticks))

diffs = []
last = ticks.pop()
while len(ticks) > 0:
    next = ticks.pop(0)
    diffs.append(ticks_diff(next, last))
    last = next

print("diffs:" + str(diffs))
avg = sum(diffs) / len(diffs)
print("avg:" + str(avg))

print("rps:" + str(avg / US_PER_SECOND))
print("rpm:" + str(avg / (US_PER_SECOND * 60.0)))
