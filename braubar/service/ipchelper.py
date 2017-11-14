import json
import posix_ipc as ipc
import signal

TYPE_TEMP = "temp"
TYPE_CONTROL = "control"
CONTROL_NEXT = "next"
CONTROL_START = "start"
CONTROL_STOP = "stop"
QUEUE_ENCODING = "utf-8"


class IPCReceiver:
    name = None
    queue = None

    def __init__(self, mq_name):
        self.name = mq_name
        self.queue = ipc.MessageQueue(name=self.name, flags=ipc.O_CREAT)
        self.queue.request_notification(signal.SIGALRM)

    def cleanup(self):
        if self.queue:
            try:
                self.queue.close()
                self.queue.unlink()
            except ipc.ExistentialError as e:
                print("IPCReceiver - cleanup:", e)
                pass

    def receive(self):
        self.queue.request_notification(signal.SIGALRM)
        msg = json.loads(self.queue.receive()[0].decode(QUEUE_ENCODING))
        return msg["type"], msg["content"]

    def close(self):
        try:
            self.queue.close()
        except Exception as e:
            print("IPCReceiver - close: ", e)


def prepare_data(msg_type, content):
    msg = {
        "type": msg_type,
        "content": content
    }
    return json.dumps(msg)

