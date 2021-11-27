import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
sys.path.pop(0)
from setuptools import setup

setup(
    name='micropython-motor-driver-dual-tb6612fng',
    py_modules=['tb6612fng'],
    version='1.1.1',
    description='MicroPython library for Motor Driver TB6612FNG boards.',
    long_description='Lets you control either or both DC motors via SparkFun Motor Driver Dual TB6612FNG boards.',
    keywords='tb6612fng motor micropython',
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