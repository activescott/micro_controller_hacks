# Milestone 1: Make the robot go forward until the ultrasonic sensor detects something within 6 CM
import uasyncio
import sys
from constants import MS_PER_SECOND, US_PER_SECOND
import drive
import display
import distance_sensor
import compass
from logger import Logger, DEBUG, INFO, WARNING, ERROR

log = None
# state machine stuff:
# states:
STATE_STARTING = "STATE_STARTING"
STATE_FORWARD = "STATE_FORWARD"
STATE_OBSTACLE_DETECTED = "STATE_OBSTACLE_DETECTED"


async def state_machine_handler(state: str) -> None | str:
    """
    Defines the type signature of a state machine handler function.
    Args: The current state.
    Returns:
      - `None` if this handler isn't responsible for handling this state (and other handlers should be attempted)
      - `str` An str indicating the new state should be returned if the handler handled the state and no other handlers should be called.
    """
    pass


async def handle_detect_obstacle(state: str) -> None | str:
    # Minimum allowed distance from an obstacle
    MIN_OBSTACLE_DISTANCE = 40.0

    distance = distance_sensor.distance()
    if distance < MIN_OBSTACLE_DISTANCE:
        log.info("handle_forward: obstacle detected in {} {} cm (min permitted is {} {}). stopped drive.".format(
            distance, type(distance), MIN_OBSTACLE_DISTANCE, type(MIN_OBSTACLE_DISTANCE)))
        return STATE_OBSTACLE_DETECTED
    elif state == STATE_OBSTACLE_DETECTED:
        log.debug(
            "handle_detect_obstacle: obstacle cleared ({} cm)".format(distance))
        return STATE_FORWARD


async def handle_avoid_obstacle(state: str) -> None | str:
    if state != STATE_OBSTACLE_DETECTED:
        return None
    drive.stop()
    drive.rotate_left_slightly()


async def handle_forward(state: str) -> None | str:
    if state != STATE_FORWARD:
        return None
    log.debug("moving forward")
    drive.forward()


async def handle_starting(state: str) -> None | str:
    if state != STATE_STARTING:
        return None
    return STATE_FORWARD


async def handle_wheel_stuck(state: str) -> None | str:
    if state == STATE_FORWARD:
        # we think we're moving so make sure that both wheels are too:
        left = drive.left_speed()
        right = drive.right_speed()
        log.debug(
            "handle_wheel_stuck: wheels left speed:{}, right speed:{}".format(left, right))

        if drive.left_stopped() or drive.right_stopped():
            log.warn(
                "handle_wheel_stuck: wheel STUCK (left speed:{}, right speed:{}). Backing up...".format(left, right))
            drive.reverse()
            await uasyncio.sleep_ms(250)
            drive.stop()


async def handle_update_display(state: str) -> None | str:
    display.update(activity=state,
                   distance=distance_sensor.distance(),
                   heading=compass.heading())


state_machine_handlers = [
    handle_starting,
    handle_detect_obstacle,
    handle_avoid_obstacle,
    handle_forward,
    handle_wheel_stuck,
    handle_update_display
]


async def state_machine_loop():
    # current state machine state:
    log.info("state machine starting...")

    current_state = STATE_STARTING
    display.update(current_state, distance=distance_sensor.distance())
    while True:
        for handler in state_machine_handlers:
            log.debug(handler.__name__ + "...")
            new_state = await handler(current_state)
            if new_state is not None and current_state != new_state:
                # handler
                log.info("sm loop: transitioning from {} to {} from handler {}".format(
                    current_state, new_state, handler.__name__))
                current_state = new_state
                display.update(activity=current_state)
                break
            else:
                continue
        await uasyncio.sleep_ms(int(MS_PER_SECOND * 0.05))


def start_logger():
    global log
    log = Logger("robot-main", level=DEBUG)


async def main():
    try:
        # wait a bit before we attempt to init devices and start moving:
        # LONG wait also allows to interrupt the bot if main.py acts up (like threads crashing sometimes bricks the pico)
        print("waiting before starting...")
        await uasyncio.sleep_ms(int(MS_PER_SECOND * 2))
        display.init()
        start_logger()
        distance_sensor.init()
        drive.init()
        compass.init()
        print("starting loop...")
        await state_machine_loop()
        print("loop returned!")
    except Exception as err:
        drive.disable()
        log.error("error in message loop", err)
    finally:
        distance_sensor.deinit()
        drive.deinit()
        display.deinit()
        sys.exit(1)


uasyncio.run(main())
