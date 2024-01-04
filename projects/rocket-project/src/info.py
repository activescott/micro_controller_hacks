import machine, esp32, os
    
def print_info():
    uname = os.uname()
    print(f"👋 My name is {uname[4]}.")
    print(f"More details about me are: {uname}")

    rtc = machine.RTC()
    print(f"To my knowledge, the time is {rtc.datetime()}")
    print(f"My ESP32 chip temperature is {esp32.raw_temperature()} fahrenheit.")
