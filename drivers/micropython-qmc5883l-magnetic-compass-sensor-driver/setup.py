import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
sys.path.pop(0)
from setuptools import setup

setup(
    name='micropython-qmc5883l-magnetic-compass-sensor-driver',
    py_modules=['qmc5883l.py'],
    version='1.0.0',
    description='MicroPython driver for the QMC5883L 3-Axis Magnetic, Digital Compass IC from QST Corporation.',
    long_description='MicroPython driver for the QMC5883L 3-Axis Magnetic, Digital Compass IC from QST Corporation (often sold as a HMC5883L as described at https://surtrtech.com/2018/02/01/interfacing-hmc8553l-qmc5883-digital-compass-with-arduino/).',
    keywords='compass magnometer micropython',
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