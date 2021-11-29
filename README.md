My adventures into lowish-level micro controller projects.

# Tools

## /tools/mpremote

These are thin wrappers around the micropython mpremote util. The most novel is `install-package.sh` which makes it easy to install a PyPi or a package from a local directory into a MicroPython device (tested only with Raspberry Pi Pico). From within the `/tools/mpremote/` directory run the following command to install the motor driver onto the device:

    $ ./install-package.sh ../../drivers/micropython-motor-driver-dual-tb6612fng/

## /tools/find-devices

Lists out the serial devices that are plugged in and running MicroPython.
