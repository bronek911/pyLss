#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name
import time
from serial import Serial


if __name__ == '__main__':
    
    print('Running. Press CTRL-C to exit.')
    with Serial("/dev/ttyUSB1", 57600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    cmd=input()
                    print(cmd == '\r\n')
                    arduino.write(bytes(cmd, 'utf-8'))
                    time.sleep(0.1) #wait for arduino to answer
                    while arduino.inWaiting()==0: pass
                    if  arduino.inWaiting()>0:
                        answer = arduino.readline()
                        while answer:
                            answer = arduino.readline()
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")
