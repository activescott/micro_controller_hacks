#!/usr/bin/env python3
# This is a python script to run on the host machine and inspect serial port devices (general those plugged into USB)
from serial.tools import list_ports
from pprint import pprint
import sys
import os

# see https://pyserial.readthedocs.io/en/latest/tools.html
if __name__ == '__main__':
    print("Listing MicroPython devices...")
    ports = list_ports.comports()
    # for more detail do this:
    # props = ['description', 'device', 'hwid', 'interface', 'location', 'manufacturer',
    #         'name', 'pid', 'product', 'serial_number', 'vid']
    #infos = [p.__dict__ for p in ports]
    # pprint(infos)
    filtered = [p for p in ports if p.manufacturer == "MicroPython"]
    for p in filtered:
        print("  " + p.device)
    print("Listing MicroPython devices complete. {} devices found".format(len(filtered)))
    dest = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../.env"))
    print("There was only one device found. Do you want to write it to `{}` (Y/n) ?".format(dest))
    for line in sys.stdin:
        if line is not None and isinstance(line, str) and line.lower().startswith("y"):
            device = filtered[0].device
            with open(dest, mode="w") as f:
                print("MP_DEVICE={}".format(device), file=f)
        break
