import os
import asyncio

#FILE='sys/bus/w1/devices/' #28-000005e2fdc3/w1_slave'
SENSORS=['test/devices/28-1/w1_slave.txt', 'test/devices/28-2/w1_slave.txt']

class Pi_Sensor:
    
    sensor_array = []

    def __init__(self, sensors):
        for sensor in sensors: 
            self.sensor_array.append((sensor,self.read_sensor_values(sensor)))
        print(self.sensor_array)
        loop.stop()

    def read_sensor_values(self, sensor_uri):
        with open(sensor_uri, "r") as f: 
            lines = f.readlines()
            return (self.status_ok(lines[0]),self.get_temp(lines[1]))

    def status_ok(self, status_str):
        if status_str.split()[-1] == 'YES':
            return True
        return False
    
    def get_temp(self, temp_str):
        temp = int(temp_str.split()[-1][2:])/1000
        return temp

    def get_sensors_count(self):
        return len(self.sensor_array)

class Sensor_Runner:

    def __init__(self, loop):
        while(True):
            try:
                Pi_Sensor(SENSORS)
            except Exception as err:
                print("Sensor_Runner:", err)
        loop.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_soon(Sensor_Runner, loop)
    loop.run_forever()
    loop.close()

