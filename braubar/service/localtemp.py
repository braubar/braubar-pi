import os
import asyncio
from brewconfig import BrewConfig
import posix_ipc as ipc
from ipchelper import prepare_data, TYPE_TEMP
import json

class Pi_Sensor:

    def __init__(self, sensors):
        sensors_count = len(sensors)
        for sensor in sensors:
            ok, temp = self.read_sensor_values(sensor["uri"])
            self.write_to_queue(temp, sensor["name"])
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

    def write_to_queue(self, temp, sensor_id):
        message_count = 0
        current_messages = 0
        queue = None
        try:
            queue = ipc.MessageQueue(name=BrewConfig.BRAUBAR_QUEUE, flags=ipc.O_CREAT)
            content = json.dumps({"temp": temp, "id": sensor_id})
            queue.send(prepare_data(TYPE_TEMP, content).encode(encoding=BrewConfig.QUEUE_ENCODING), timeout=5)
            current_messages = queue.current_messages
            message_count += 1
            print("current messages: ", queue.current_messages,
                  "max_messages: ", queue.max_messages,
                  "max_message_size", queue.max_message_size)

        except ipc.ExistentialError:
            return False
        except ipc.BusyError as bse:
            print("socket busy Error: Queue reached limit", bse)
            return False
        except OSError as ose:
            print("OSERROR: ",ose)
            print("current_messages: ", current_messages)
        finally:
            if queue is not None:
                queue.close()

        return True

class Sensor_Runner:

    def __init__(self, loop, sensors):
        while(True):
            try:
                Pi_Sensor(sensors)
            except Exception as err:
                print(sensors)
                print("Sensor_Runner:", err)
        loop.stop()

if __name__ == "__main__":
    config = BrewConfig()
    sensors_config = config.get("sensors")
    loop = asyncio.get_event_loop()
    try:
        loop.call_soon(Sensor_Runner, loop, sensors_config)
        loop.run_forever()
    except:
        pass
    finally:
        loop.close()
