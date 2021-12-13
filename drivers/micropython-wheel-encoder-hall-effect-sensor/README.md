# micropython-wheel-encoder-hall-effect-sensor

MicroPython driver for [SparkFun's Wheel Encoder Kit's hall effect sensor](https://www.sparkfun.com/products/12629).

## Usage
NOTE That this library uses an asyncio coroutine to read the sensor so your main app must use `uasyncio.run(main())` and yield to uasyncio periodically like `await uasyncio.sleep_ms(5)` (note the await!)
See the examples folder for a complete example.
```py
async def main():
    # setup
    motors = init_motors()
    print("setting up encoder")
    with Encoder(WHEEL_ENCODER_PIN_RIGHT) as encoder:
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

```
