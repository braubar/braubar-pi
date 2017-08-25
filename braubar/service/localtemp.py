import os 

#FILE='sys/bus/w1/devices/28-000005e2fdc3/w1_slave'
FILE='sensor_temp_dummy.txt'

class Pi_Sensor:
    
    sensor_array = []

    def __init__(self, sensors):
        sensor_array = []
        for sensor in sensors: 
            sensor_array.append((sensor,self.read_sensor_values(sensor)))

    def read_sensor_values(self, sensor_uri):
        with open(sensor_uri, "r") as f: 
            lines = f.readlines()
            return (lines[0],lines[1])

    def status_ok(self, status_str):
        if status_str.split()[-1] == 'YES':
            return True
        return False
    
    def get_temp(self, temp_str):
        temp = int(temp_str.split()[-1][2:])/1000
        return temp

if __name__ == "__main__":
    pi = Pi_Sensor([FILE])
    s_str, t_str = pi.read_sensor_values(FILE)
    s = pi.status_ok(s_str)
    t = pi.get_temp(t_str)
    print(s)
    print(t)
