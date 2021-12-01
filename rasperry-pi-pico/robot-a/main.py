# Milestone 1: Make the robot go forward until the ultrasonic sensor detects something within 6 CM
import utime
from constants import MS_PER_SECOND, US_PER_SECOND, MIN_OBSTACLE_DISTANCE
import drive
import distance_sensor
from logger import Logger, DEBUG, INFO, WARNING, ERROR

log = None
# state machine stuff:
# states:
STATE_STARTING = "STATE_STARTING"
STATE_FORWARD = "STATE_FORWARD"
STATE_OBSTACLE_DETECTED = "STATE_OBSTACLE_DETECTED"


def state_machine_handler(state: str) -> None | str:
    """
    Defines the type signature of a state machine handler function.
    Args: The current state.
    Returns:
      - `None` if this handler isn't responsible for handling this state (and other handlers should be attempted)
      - `str` An str indicating the new state should be returned if the handler handled the state and no other handlers should be called.
    """
    pass


def handle_forward(state: str) -> None | str:
    if state != STATE_FORWARD:
        return None
    distance = distance_sensor.distance()
    if distance < MIN_OBSTACLE_DISTANCE:
        drive.stop()
        log.info("handle_forward: obstacle detected in {} {} cm (min permitted is {} {}). stopped drive.".format(
            distance, type(distance), MIN_OBSTACLE_DISTANCE, type(MIN_OBSTACLE_DISTANCE)))
        return STATE_OBSTACLE_DETECTED
    else:
        log.debug(
            "handle_forward: no obstacle detected ({} cm)".format(distance))


def handle_starting(state: str) -> None | str:
    if state != STATE_STARTING:
        return None
    drive.forward()
    return STATE_FORWARD


def handle_obstacle(state: str) -> None | str:
    if state != STATE_OBSTACLE_DETECTED:
        return None
    distance = distance_sensor.distance()
    if distance > MIN_OBSTACLE_DISTANCE:
        log.info(
            "handle_obstacle: obstacle removed ({} cm). moving...".format(distance))
        drive.forward()
        return STATE_FORWARD
    else:
        log.debug(
            "handle_obstacle: still see obstacle at {} cm. avoiding...".format(distance))
        drive.rotate_left_slightly()
        return STATE_OBSTACLE_DETECTED


state_machine_handlers = [
    handle_starting,
    handle_obstacle,
    handle_forward
]


def state_machine_loop():
    # current state machine state:
    log.info("state machine starting...")
    current_state = STATE_STARTING
    while True:
        for handler in state_machine_handlers:
            print(handler.__name__ + "...")
            new_state = handler(current_state)
            if new_state is not None and current_state != new_state:
                # handler
                print("transition...")
                log.info("sm loop: transitioning from {} to {} from handler {}".format(
                    current_state, new_state, handler.__name__))
                current_state = new_state
                break
            else:
                continue
        #utime.sleep_us(int(US_PER_SECOND * 0.01))

# general setup & start:


def start_logger():
    global log
    log = Logger("robot-main", level=DEBUG)
    log.open()


def main():
    # wait a bit before we attempt to init devices and start moving:
    # LONG wait also allows to interrupt the bot if main.py acts up (like threads crashing sometimes bricks the pico)
    utime.sleep_ms(int(MS_PER_SECOND * 3))
    start_logger()
    distance_sensor.setup()
    drive.setup()
    state_machine_loop()


main()
