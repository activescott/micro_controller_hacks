# microcontroller-hacks

My adventures into lowish-level microcontroller projects.

## Drivers

Here are some drivers I have created or forked:

- [drivers/micropython-motor-driver-dual-tb6612fng](drivers/micropython-motor-driver-dual-tb6612fng) contains A MicroPython driver for [SparkFun Motor Driver - Dual TB6612FNG boards](https://www.sparkfun.com/products/14450) that use the Toshiba TB6612FNG IC. There is support for one or two ICs.
- [drivers/micropython-open-lcd-driver](drivers/micropython-open-lcd-driver) contains a MicroPython driver for [SparkFun OpenLCD-firmware LCD displays](https://github.com/sparkfun/OpenLCD) such as the [SparkFun 16x2 SerLCD - RGB Backlight](https://www.sparkfun.com/products/16396).
- [drivers/micropython-qmc5883l-magnetic-compass-sensor-driver](drivers/micropython-qmc5883l-magnetic-compass-sensor-driver) contains a MicroPython driver for the QMC5883L 3-Axis Magnetic, Digital Compass IC from QST Corporation (often sold as a HMC5883L).
- [drivers/micropython-wheel-encoder-hall-effect-sensor](drivers/micropython-wheel-encoder-hall-effect-sensor) contains a MicroPython driver for [SparkFun's Wheel Encoder Kit's hall effect sensor](https://www.sparkfun.com/products/12629).
- Forked https://github.com/rsc1975/micropython-hcsr04 with some fixes for recent versions MicroPython. The full repo is at https://github.com/activescott/micropython-hcsr04 but I do submodule it here for easy use in this repo.

## Projects

Most of the projects in the [projects/](projects/) folder are basic walkthroughs or one-off experiments with a particular sensor or device. [projects/robot-a](projects/robot-a) contains one of my more ambitious projects so far.

## Tools

### /tools/mpremote

These are thin wrappers around the [MicroPython mpremote util](https://docs.micropython.org/en/latest/reference/mpremote.html). The most novel is `install-package.sh` which makes it easy to install a PyPi or a package from a local directory into a MicroPython device (tested only with Raspberry Pi Pico). From within the `/tools/mpremote/` directory run the following command to install the motor driver onto the device:

    $ ./install-package.sh ../../drivers/micropython-motor-driver-dual-tb6612fng/

### /tools/find-devices

Lists out the serial devices that are plugged in and running MicroPython.
