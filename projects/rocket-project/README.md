# Rocket Project

This is a family project to collect altitude and environmental data from a rocket we'll launch.

We are using MicroPython to make sure it's approachable enough for kids and other non-experts: https://docs.micropython.org/en/latest/esp32/tutorial/intro.html#

NOTE: Also evaluated ESPHome (no SD Card support) and PlatformIO (too complex UI in VSCode for kids) and Arduino+IDE (not bad, just choosing MicroPython mostly for language choice).

## Using an Olimex ESP32-POE

[Olimex ESP32-PoE](https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/open-source-hardware).

MicroPython Page: https://micropython.org/download/OLIMEX_ESP32_POE/

It reports the following from esptool.py:

```sh
$ esptool.py get_security_info
esptool.py v4.7.0
Found 3 serial ports
Serial port /dev/cu.usbserial-1420
Connecting....
Detecting chip type... Unsupported detection protocol, switching and trying again...
Connecting....
Detecting chip type... ESP32
Chip is ESP32-D0WD-V3 (revision v3.0)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: e0:5a:1b:65:49:08
Uploading stub...
Running stub...
Stub running...

A fatal error occurred: Failed to get security info (result was FF00: Command not implemented)
```

## Usage

Essentially following https://docs.micropython.org/en/latest/esp32/tutorial/intro.html#
with python3 installed, use `pip3 install esptool` which installs `esptool.py` in your path.

### Flashing the Board

We "Flash" a board meaning we erase anything on the board and replace it with a new "firmware". The firmware is the code on the board that runs as soon as it turns on and in turn can load other code. We will erase it and flash it with the MicroPython firmware for our ESP32-based board

Terms:

- ESP32 is the name of the chip/processor that is on our particular board (as well as many other types of boards).

First erase it by running the command below in the terminal:

_NOTE: You only run the commands after the `$` symbol. What follows that line is the output that I saw when I ran the command._

```sh
$ esptool.py erase_flash

esptool.py v4.7.0
Found 3 serial ports
Serial port /dev/cu.usbserial-1420
Connecting......
Detecting chip type... Unsupported detection protocol, switching and trying again...
Connecting......
Detecting chip type... ESP32
Chip is ESP32-D0WD-V3 (revision v3.0)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: e0:5a:1b:65:49:08
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
ddChip erase completed successfully in 13.6s
Hard resetting via RTS pin...
```

Now we'll download the firmware from https://www.micropython.org/download/OLIMEX_ESP32_POE/ copy it to a local directory (I am putting it in /vendor/micropython-firmware/OLIMEX_ESP32_POE-20231227-v1.22.0.bin)
Then copy the downloaded MicroPython firmware to it:

```sh
$ esptool.py --chip esp32 --baud 460800 write_flash -z 0x1000 ./vendor/micropython-firmware/OLIMEX_ESP32_POE-20231227-v1.22.0.bin

esptool.py v4.7.0
Found 3 serial ports
Serial port /dev/cu.usbserial-1420
Connecting....
Chip is ESP32-D0WD-V3 (revision v3.0)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: e0:5a:1b:65:49:08
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Flash will be erased from 0x00001000 to 0x001a9fff...
Compressed 1737648 bytes to 1143583...
Wrote 1737648 bytes (1143583 compressed) at 0x00001000 in 28.6 seconds (effective 486.7 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```

### Verifying It Worked!

Then to verify it works, open up [thonny](https://thonny.org/) (can install with homebrew) and use the bottom right corner status bar button to open up a terminal to the detected serial port and you can get a REPL to the board.

Terms:

- REPL: This just means you can type in Python code and as you type it it will run immediately and show you the result. When you run code in this Thonny window, the code will run _on the board/device_ it won't be running on your computer.

_NOTE: For more advanced usage you can also do this without thonny using [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html)._

Some simple ESP32 specific functions (mostly from https://docs.micropython.org/en/latest/esp32/quickref.html):

```py
import esp32

temp = esp32.raw_temperature()
print(f"The ESP32 temperature is currently {temp}f")
```

To scan the i2c Bus:

```py
from machine import Pin, I2C
i2c = I2C(1, scl=Pin(16), sda=Pin(13), freq=400000)
devices = i2c.scan()
for dev in devices:
  print(f"found device {dev}")
```

## Developing Your Program

To develop our program we create and edit files in the `./src` folder here. THen we'll run some commands to "run" those files on the device.
While we're developing and making things work we'll "mount" the `./src` folder and its files on the device. This just means that the device will think those files are instantly and always copied to the device. Code that is used with a "mount" only works while the device is plugged into our computer though. Once we want to run it with it disconnected, we'll have to copy the code to the device. To do that we'll call say we **deploy** the code to the device. Lets walk through each below...

👋
