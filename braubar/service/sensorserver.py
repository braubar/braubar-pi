import json
from socketserver import UDPServer, DatagramRequestHandler
from brewconfig import BrewConfig
import posix_ipc as ipc

import os

SYNC_BITS = b'\x0f\x00\x0f\x0f'
TEMP_RAW_FILE = "../data/temp.brew"


class Handler(DatagramRequestHandler):
    def handle(self):
        raw_data = bytearray(self.request[0])
        start_sync = raw_data[:4]
        temp = (raw_data[4] | raw_data[5] << 8) / 100
        id_data = int(raw_data[6])
        end_sync = raw_data[7:]
        if start_sync == end_sync == SYNC_BITS:
            self.write_to_queue(temp, id_data)

    def write_to_queue(self, temp, id_data):
        try:
            queue = ipc.MessageQueue(name=BrewConfig.TEMP_QUEUE)
            queue.send(json.dumps({"temp": temp, "id": id_data}).encode(encoding=BrewConfig.QUEUE_ENCODING), timeout=1)
        except ipc.ExistentialError:
            queue.close()
            return False
        except ipc.BusyError:
            print("socket busy")
            queue.close()
            return False
        return True

    def write_to_file(self, temp, id_data):
        f = open(TEMP_RAW_FILE, mode='a')
        s = str(id_data) + ':' + str(temp) + os.linesep
        f.write(s)
        f.close()
        # TODO speichern!
        print("message:", s)
        print("id:", int(id_data))
        print("from:", self.client_address)


class SensorServer:
    def start(self):
        addr = ("", 50505)
        print("listening on %s:%s" % addr)

        server = UDPServer(addr, Handler)
        server.serve_forever()


if __name__ == "__main__":
    server = SensorServer()
    server.start()
