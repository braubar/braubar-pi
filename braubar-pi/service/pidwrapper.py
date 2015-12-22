from PID import PID
from threading import Thread, Timer


class PIDWrapper(PID):
    pid = None
    thread = None

    def __init__(self):
        self.thread = Thread(target=self.do_work, name="BrewPID", args=())

    def update(self, feedback_value):
        self.pid.update(feedback_value)

    def start(self):
        self.thread.run()

        # assert 0

    def do_work(self):
        self.pid = PID(0.2, 0.0, 0.0)
        print("PID started")
