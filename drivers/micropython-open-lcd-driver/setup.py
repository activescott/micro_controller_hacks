import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
sys.path.pop(0)
from setuptools import setup

setup(
    name='micropython-open-lcd-driver',
    py_modules=['tb6612fng'],
    version='1.0.0',
    description='MicroPython driver for OpenLCD displays.',
    long_description='A MicroPython driver for SparkFun OpenLCD-firmware LCD displays such as the SparkFun 16x2 SerLCD - RGB Backlight.',
    keywords='OpenLCD SerLCD SparkFun LCD micropython',
    url='https://github.com/activescott/micro_controller_hacks',
    author='Scott Willeke',
    author_email='scott@willeke.com',
    maintainer='Scott Willeke',
    maintainer_email='scott@willeke.com',
    license='MIT',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: Implementation :: MicroPython',
        'License :: OSI Approved :: MIT License',
    ],
)