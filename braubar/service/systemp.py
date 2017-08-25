# -*- coding: utf-8 -*-
import os

# SENSOR_NAME = "28-011581adc2ff"
# TEMP_DIR = "/sys/bus/w1/devices/"
SENSOR_NAME = "28-1"
TEMP_DIR = "../../test/w1/"



filename = TEMP_DIR + SENSOR_NAME + "/w1_slave"
with open(filename, 'r') as f:
    a = f.readlines()
    if (a[0][:-3]=='YES'):
            print("crc OK")
    b = a[1].split()
    print(int(b[-1][2:])/1000.0)
