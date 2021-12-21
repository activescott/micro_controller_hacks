import uasyncio
from array import array
from machine import Pin
from micropython import const
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
        self.pin_val_last = -1
        self._reader_irq_handler_setup()

    def cancel(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cancel()

    def _reader_irq_handler_setup(self):
        self.pin.irq(handler=self._reader_irq_handler,
                     trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True)

    def _hit(self, pin_val):
        if pin_val == _MAGNET_DETECTED and pin_val != self.pin_val_last:
            self._speed_track_hit()
            self._hits += 1
        self.pin_val_last = pin_val

    def _reader_irq_handler(self, pin_instance):
        # Here we read the pin very frequently as called by an IRQ. Couple weird things happen:
        # 1. We'll read hits with the same value rapidly
        # 2. We also only want to record a hit if MAGNET_DETECTED is directly preceded by a NOT DETECTED. Otherwise when the wheel is stopped with the magnet directly on top of the sensor we will think the wheel is still moving.
        # To mitigate both we ensure MAGNET_DETECTED is only recorded if it was preceded by not detected. A "not detected" event is only recorded to know if it directly preceded a detected event.
        self._hit(pin_instance.value())

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
                # we've slowed; assume a rotation duration takes this long (but it could take longer in practice)
                one_rotation_duration = since * self.hits_per_rotation
        _ONE_MINUTE = const(_MS_PER_SECOND * 60)
        return _ONE_MINUTE / one_rotation_duration

    def __repr__(self) -> str:
        return "Encoder (hits: {hits})".format(hits=self.hits())
