import socket
import random
import time
import os
import atexit
import signal

UDP_IP = "0.0.0.0"
UDP_PORT = 50505
MESSAGE = b'\x0f\x00\x0f\x0fr\x08\x06\x0f\x00\x0f\x0f'
SYNC_BITS = b'\x0f\x00\x0f\x0f'


class SensorDummy():

    def __init__(self):
        print("UDP target IP:", UDP_IP)
        print("UDP target port:", UDP_PORT)
        print("message:", MESSAGE)

    def prepare_message(self, sensor_id, temp):
        message = SYNC_BITS
        message += bytes([int(temp * 100) & 0x00FF])
        message += bytes([(int(temp * 100) >> 8) & 0x00FF])
        message += bytes([sensor_id])
        message += SYNC_BITS

        return message

    def send(self, sensor_id, temp):
        message = self.prepare_message(sensor_id, temp)
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.sendto(message, (UDP_IP, UDP_PORT))

#        print(message)

    def run(self, sensor_id=99, temp=20.1):
        self.send(sensor_id=sensor_id, temp=temp)


sensor = SensorDummy()

count = 0

while True:
    sensor_id = random.randint(10, 15)
    temp = round(random.uniform(30, 52), 2)
    sensor.run(sensor_id=sensor_id, temp=temp)
    count += 1
    if count % 1000 == 0:
        print("count: ", count)
    time.sleep(0)
