# Raspberry Pi Pico with RP2040

My adventures with MicroPython on Raspberry Pi Pico with RP2040.

## Hardware:

- [Raspberry Pi's docs for the Pico](https://www.raspberrypi.com/documentation/) are great.
- Pinout: https://www.raspberrypi.com/documentation/microcontrollers/images/Pico-R3-SDK11-Pinout.svg

## MicroPython

- Using [MicroPython](https://micropython.org/)
- [MicroPython Libraries Reference](https://docs.micropython.org/en/latest/library/index.html)
- [https://github.com/raspberrypi/pico-micropython-examples](Raspberry Pi's provided examples w/ MicroPython)

### [Thonny IDE](https://thonny.org/)

- Primary reason for using this is because it makes nice REPL and uploading code to MicroPython devices super fast. The alternative is [mpremote command line tool](https://docs.micropython.org/en/latest/reference/mpremote.html).
- Be sure to Select **Files** from the **View** main menu!

### mpremote: Interacting with a MicroPython Device from shell

Usage docs at https://docs.micropython.org/en/latest/reference/mpremote.html

List devices:

    mpremote connect list

Connect to the device:

    mpremote connect <device-port>

Get `<device-port>` from the first column of the list from the `mpremote connect list` command.

Once you connect you're put into a REPL python environment on the device. You can enter something like `os.uname()` to see some output about the device python is running in.

## Misc References:

- Tensorflow Light: https://www.raspberrypi.com/documentation/accessories/camera.html#post-processing-with-tensorflow-lite
- Find micropython packages at https://pypi.org/search/?c=Programming+Language+%3A%3A+Python+%3A%3A+Implementation+%3A%3A+MicroPython

## Creating MicroPython Packages

Mostly like creating a normal package.

- Prefix package name with `micropython-...`
- Be sure to include the `Python :: Implementation :: MicroPython` in classifiers array in setup.py

## Using MicroPython Packages & MicroPython Unix

You can use MicroPython Unix to prepare packages and apps for distribution to a device. There is a docker image of it at https://hub.docker.com/r/micropython/unix. See [Cross-installing packages](https://docs.micropython.org/en/latest/reference/packages.html#cross-installing-packages)

Start an interactive session with micropython unix like `docker run -it "micropython/unix"`

### Examples for reference:

- https://github.com/mcauser/micropython-ssd1327
- https://github.com/HeMan/micropython-ws2801
- https://github.com/tuupola/micropython-mpu6886 (shows up in pipy well, good examples, but shows WIP)
- https://github.com/fizista/micropython-umqtt.simple2 sophisticated setup.py to minimize package

## How to unbrick your MicroPython Raspberry Pi Pico

Download the firmware at https://forums.raspberrypi.com/viewtopic.php?f=146&t=305432 and copy it on there. It is a MicroPython derivative that will rename main.py to main-1.py or something and then you can boot it normally. Then open Thonny, go to Options and on the "Interpreter" Options tab, you can select **Install or update firmware**.
Found at https://forum.micropython.org/viewtopic.php?f=21&t=10095
There is also a nuke program from Raspberry Pi at https://github.com/raspberrypi/pico-examples/blob/master/flash/nuke/nuke.c
