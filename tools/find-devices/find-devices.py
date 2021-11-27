#!/usr/bin/env python3
# This is a python script to run on the host machine and inspect serial port devices (general those plugged into USB)
from serial.tools import list_ports
from pprint import pprint

# see https://pyserial.readthedocs.io/en/latest/tools.html
if __name__ == '__main__':
    print("Finding MicroPython devices...")
    ports = list_ports.comports()
    # for more detail do this:
    #props = ['description', 'device', 'hwid', 'interface', 'location', 'manufacturer',
    #         'name', 'pid', 'product', 'serial_number', 'vid']
    #infos = [p.__dict__ for p in ports]
    #pprint(infos)
    filtered = [p for p in ports if p.manufacturer=="MicroPython"]
    for p in filtered:
        print("  " + p.device)
