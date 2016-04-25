import json
from socketserver import UDPServer, DatagramRequestHandler
from brewconfig import BrewConfig
import posix_ipc as ipc
from ipchelper import prepare_data, TYPE_TEMP

SYNC_BITS = b'\x0f\x00\x0f\x0f'


class Handler(DatagramRequestHandler):
    def handle(self):
        raw_data = bytearray(self.request[0])
        start_sync = raw_data[:4]
        temp = (raw_data[4] | raw_data[5] << 8) / 100
        id_data = int(raw_data[6])
        end_sync = raw_data[7:]
        if start_sync == end_sync == SYNC_BITS:
            self.write_to_queue(temp, id_data)

    def write_to_queue(self, temp, sensor_id):
        try:
            queue = ipc.MessageQueue(name=BrewConfig.BRAUBAR_QUEUE)
            content = json.dumps({"temp": temp, "id": sensor_id})
            queue.send(prepare_data(TYPE_TEMP, content).encode(encoding=BrewConfig.QUEUE_ENCODING), timeout=1)
        except ipc.ExistentialError:
            queue.close()
            return False
        except ipc.BusyError:
            print("socket busy")
            queue.close()
            return False
        return True


class SensorServer:
    def start(self):
        addr = ("", 50505)
        print("listening on %s:%s" % addr)

        sensor_server = UDPServer(addr, Handler)
        sensor_server.serve_forever()


if __name__ == "__main__":
    server = SensorServer()
    server.start()
