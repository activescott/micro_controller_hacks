import uasyncio
from array import array
from machine import Pin
from funcs import debounce1 as debounce
from utime import ticks_diff, ticks_ms

_MS_PER_SECOND = const(1000)

# the sensor is indicating a magnet when voltage is low/0
_MAGNET_DETECTED = const(0)
_MAGNET_NOT_DETECTED = const(1)


class Encoder:
    """
    Represents a wheel encoder/hall effect sensor.
    I'm using this with SmarkFun's Wheel Encoder Kit - ROB-12629.
    NOTE: This leverages uasyncio so your main app must use `uasyncio.run(main()) and yield to uasyncio periodically like `await uasyncio.sleep_ms(5)` (note the await!)
    """

    def __init__(self, pin_id, hits_per_rotation=4):
        _INITIAL_VAL = _MAGNET_NOT_DETECTED
        self.pin = Pin(pin_id, mode=Pin.IN,
                       pull=Pin.PULL_UP, value=_INITIAL_VAL)
        self.hits_per_rotation = hits_per_rotation
        self._hits = 0
        self._reader_task = None
        # we estimate speed by looking at time between two hits and if the time of request is within that duration (before the subsequent hit) then we estimate we're still moving
        self._last_hit_time = -1
        self._last_hit_duration = -1
        # get started:
        self.run()

    def run(self):
        # NOTE: this only works if the main app uses uasyncio.run(...) and yield to uasyncio like `await uasyncio.sleep_ms(5)` (note the await!)
        if self._reader_task is None:
            self._reader_task = uasyncio.create_task(self._reader())
        return self._reader_task

    def cancel(self):
        if self._reader_task is not None:
            # TODO: needs a try/except?
            self._reader_task.cancel()
            self._reader_task = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cancel()

    async def _reader(self):
        # Here we read the pin in a loop. Couple weird things happen:
        # 1. We'll read hits with the same value rapidly
        # 2. We also only want to record a hit if MAGNET_DETECTED is directly preceded by a NOT DETECTED. Otherwise when the wheel is stopped with the magent directly on top of the sensor we will think the wheel is still moving.
        # To mitigate #1 we use a debounce
        # To mitigate #2, we ensure MAGNET_DETECTED is only recorded if it was preceded by not detected.
        pin_val_last = -1

        def _hit(pin_val):
            nonlocal pin_val_last
            if pin_val == _MAGNET_DETECTED and pin_val != pin_val_last:
                self._speed_track_hit()
                self._hits += 1
            pin_val_last = pin_val

        debounced_hit = debounce(_hit, time_window_ms=1000)
        while True:
            pin_val = self.pin.value()
            debounced_hit(pin_val)
            await uasyncio.sleep_ms(5)

    def _speed_track_hit(self):
        now = ticks_ms()
        new_duration = ticks_diff(now, self._last_hit_time)
        self._last_hit_duration = new_duration
        self._last_hit_time = now

    def hits(self):
        return self._hits

    def speed(self) -> int:
        "returns speed in rotations per minute"
        now = ticks_ms()
        since = ticks_diff(now, self._last_hit_time)
        #print("since: {}, last: {}".format(since, self._last_hit_duration))
        if since <= self._last_hit_duration:
            # use the duration between two hits to estimate speed:
            one_rotation_duration = self._last_hit_duration * self.hits_per_rotation
        else:
            # it's been a while since the last hit, so we've either slowed down or stopped:
            if since >= self._last_hit_duration * 2:
                # we've slowed significantly (arbitrary factor); assume we've STOPPED. This could cause a blip if we're still moving, but slowed dramatically, but that should be rectified in 2 hits so this will appear as only a very brief stop.
                self._last_hit_duration = -1
                self._last_hit_time = -1
                return 0
            else:
                # if we've slowed, it's /at least/ this long to do a rotation:
                one_rotation_duration = since * self.hits_per_rotation
        _ONE_MINUTE = const(_MS_PER_SECOND * 60)
        return _ONE_MINUTE / one_rotation_duration

    def __repr__(self) -> str:
        return "Encoder (hits: {hits})".format(hits=self.hits())
