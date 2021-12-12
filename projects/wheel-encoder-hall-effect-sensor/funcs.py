from machine import Timer


def debounce1(func, time_window_ms=10):
    """
    Debounce for a function with a single arg
    When multiple calls call a function with the same argument values in a given time window (defined by `time_window_us`), only a single call will be forwarded to the original function.

    Arguments:
      - `func`: The function to debounce
      - `time_window_us`: The time window in microseconds that successive calls will be debounced during.

    Returns: 
        A new function to be called instead of the original.

    Notes:
        The call is forwarded when the time window defined by `time_window_us` has expired or the argument values for a call are different than the prior call.
    """
    last_arg1 = None
    timer: Timer = Timer()
    is_in_window: bool = False

    def _call_orig(timer=None):
        "Used when the debouncer window closes"
        nonlocal func, is_in_window, last_arg1
        is_in_window = False
        func(last_arg1)
        last_arg1 = None

    def debouncer(arg1):
        nonlocal func, is_in_window, last_arg1, timer
        if not is_in_window:
            # we're not already in a debouncing window, so just set one up
            # ...when the window expires the timer will make the call:
            last_arg1 = arg1
            timer.init(period=time_window_ms,
                       mode=Timer.ONE_SHOT, callback=_call_orig)
            is_in_window = True
            return
        else:
            # we are in debouncing window, so we have to compare args:
            if last_arg1 == arg1:
                # we're in a window and args are the same, just wait on the next timeout
                pass
            else:
                # we're in a window but args are different: so we need to cancel our timer and call it:
                timer.deinit()
                _call_orig()
                pass
        pass

    return debouncer
