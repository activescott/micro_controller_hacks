
# https://docs.micropython.org/en/latest/library/machine.SDCard.html#machine-sdcard
# From the Olimex ESP32-POE-user-manual.pdf:
#  GPIO2, GPIO14, GPIO15 are used for the SD-card, if no SD card they are free to use
# MicroPython (doc url above) lists "Slot 1" as sck=14, cmd=15, D0=2, D1=4, D2=12, D3=13

import machine, os, time

# Slot 1 uses pins sck=14, cs=?, miso=?, mosi=?
sd = machine.SDCard(slot=1)

def list_test():
    print('mounting...')
    os.mount(sd, '/sd')
    print('listing...')
    os.listdir('/sd')
    print('unmount...')
    os.umount('/sd')
    print('unmount complete.')

def write_test():
    os.mount(sd, '/sd')
    
    with open('/sd/test.log', 'at', encoding='utf-8') as file:
      tt = time.localtime()[3:6]
      now = "{:02d}:{:02d}.{:02d} ".format(*tt)
      file.write(f'Hello World {now}\n')
    
    print('write complete. listing files:')
    os.listdir('/sd')
    
    os.umount('/sd')
    print('unmount complete.')

def read_test():
    os.mount(sd, '/sd')
    
    with open('/sd/test.log', 'rt', encoding='utf-8') as file:
        contents = file.read()
    print('read the following from file:\n', contents)        
    
    os.umount('/sd')

if __name__ == '__main__':
    #list_test()
    write_test()
    read_test()