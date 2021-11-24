# Getting Started with MicroPython on Raspberry Pi Pico, Chapter 5...
# Traffic Light Controller
import machine
import utime
import _thread


led_red = machine.Pin(15, machine.Pin.OUT)
led_yellow = machine.Pin(14, machine.Pin.OUT)
led_green = machine.Pin(13, machine.Pin.OUT)

button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
buzzer = machine.Pin(12, machine.Pin.OUT)

# globals for cross-thread communication:
global button_pressed
button_pressed = False


# secondary thread:
def button_reader_thread():
    global button_pressed
    while True:
        if button.value() == 1:
            print("button reader: button pressed!")
            button_pressed = True
        utime.sleep(0.01)

_thread.start_new_thread(button_reader_thread, ())

# main loop:
while True:
    if button_pressed == True:
        print("main thread: button pressed!")
        led_red.value(1)
        for i in range(10):
            buzzer.value(1)
            utime.sleep(0.2)
            buzzer.value(0)
            utime.sleep(0.2)
        global button_pressed
        button_pressed = False
    
    # red on
    led_red.value(1)
    utime.sleep(5)
    
    # yellow on
    led_yellow.value(1)
    utime.sleep(2)
    
    # green on
    led_red.value(0)
    led_yellow.value(0)
    led_green.value(1)
    utime.sleep(5)
    
    # yello on
    led_green.value(0)
    led_yellow.value(1)
    utime.sleep(5)
    
    led_yellow.value(0)


