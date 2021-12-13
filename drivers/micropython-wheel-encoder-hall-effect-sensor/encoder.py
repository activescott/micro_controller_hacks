import uasyncio
from array import array
from machine import Pin
from funcs import debounce1 as debounce

# the sensor is indicating a magnet when voltage is low/0
_MAGNET_DETECTED = const(0)
_MAGNET_NOT_DETECTED = const(1)


class Encoder:
    """
    Represents a wheel encoder/hall effect sensor.
    I'm using this with SmarkFun's Wheel Encoder Kit - ROB-12629.
    NOTE: This leverages uasyncio so your main app must use `uasyncio.run(main()) and yield to uasyncio periodically like `await uasyncio.sleep_ms(5)` (note the await!)
    """

    def __init__(self, pin_id):
        _INITIAL_VAL = _MAGNET_NOT_DETECTED
        self.pin = Pin(pin_id, mode=Pin.IN,
                       pull=Pin.PULL_UP, value=_INITIAL_VAL)
        self._hits = 0
        self._reader_task = None
        self.run()

    def run(self):
        # NOTE: this only works if the main app uses uasyncio.run(...) and yield to uasyncio like `await uasyncio.sleep_ms(5)` (note the await!)
        if self._reader_task is None:
            self._reader_task = uasyncio.create_task(self._reader())
        return self._reader_task

    def cancel(self):
        if self._reader_task is not None:
            # TODO: this probably needs a try/except?
            self._reader_task.cancel()
            self._reader_task = None

    # TODO: add __exit__ so it can be used with `with`
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cancel()

    async def _reader(self):
        "Here we read the pin in a loop"
        setter = debounce(self._hit, time_window_ms=1000)
        while True:
            pin_val = self.pin.value()
            setter(pin_val)
            await uasyncio.sleep_ms(5)

    def _hit(self, pin_val):
        if pin_val == _MAGNET_DETECTED:
            self._hits += 1

    def hits(self):
        return self._hits

    def __repr__(self) -> str:
        return "Encoder (hits: {hits})".format(hits=self.hits())
