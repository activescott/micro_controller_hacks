import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
sys.path.pop(0)
from setuptools import setup

setup(
    name='micropython-wheel-encoder-hall-effect-sensor',
    py_modules=['encoder.py', 'funcs.py'],
    version='1.0.0',
    description='MicroPython driver for SparkFun\'s Wheel Encoder Kit\'s hall effect sensor.',
    long_description='MicroPython driver for [SparkFun\'s Wheel Encoder Kit\'s hall effect sensor](https://www.sparkfun.com/products/12629).',
    keywords='hall-effect-sensor wheel-encoder micropython',
    url='https://github.com/activescott/micro_controller_hacks',
    author='Scott Willeke',
    author_email='scott@willeke.com',
    maintainer='Scott Willeke',
    maintainer_email='scott@willeke.com',
    license='MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: Implementation :: MicroPython',
        'License :: OSI Approved :: MIT License',
    ],
)