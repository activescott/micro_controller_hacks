import uasyncio
from constants import WHEEL_ENCODER_PIN_LEFT
from encoder import Encoder

async def main():
    # setup
    encoder = Encoder(WHEEL_ENCODER_PIN_LEFT)

    # main: just manually move the wheel/motor and see how much it detects
    for seconds in range(5, 0, -1):
        print("waiting {} seconds...".format(seconds))
        print("hit count: " + str(encoder.hits()))
        await uasyncio.sleep_ms(1000)

    print("Final hit count: " + str(encoder.hits()))
    print(encoder)

uasyncio.run(main())
