import json
import posix_ipc as ipc

TYPE_TEMP = "temp"
TYPE_CONTROL = "control"
CONTROL_NEXT = "next"
CONTROL_START = "start"
QUEUE_ENCODING = "utf-8"

class IPCReceiver:
    name = None
    queue = None

    def __init__(self, mq_name):
        self.name = mq_name
        self.queue = ipc.MessageQueue(name=self.name, flags=ipc.O_CREAT)
        while True:
            try:
                self.queue.receive(0)
            except ipc.BusyError as e:
                print("ipchelper:", e)
                break
            except ipc.Error:
                print("error: ")
            except Exception as e:
                print("ipchelper: ", e)

    def cleanup(self):
        if self.queue:
            try:
                self.queue.close()
                self.queue.unlink()
            except ipc.ExistentialError as e:
                print("ipchelper:", e)
                pass

    def receive(self):
        msg = json.loads(self.queue.receive()[0].decode(QUEUE_ENCODING))
        return msg["type"], msg["content"]


def prepare_data(msg_type, content):
    msg = {
        "type": msg_type,
        "content": content
    }
    return json.dumps(msg)
