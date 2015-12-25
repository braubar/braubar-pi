#from PID import PID as PID
from PIDs import Pid as PID
from threading import Thread, Timer


class PIDWrapper():
    pid = None
    thread = None

    def __init__(self, temp=45.0, below=-0.5, above=0.5):
        self.temp = temp
        self.thread = Thread(target=self._do_work, name="BrewPID", args=())

    def update(self, set):
        self.pid.set(set)
    def start(self):
        self.thread.run()

        # assert 0

    def get(self):
        self.pid.get()

    def _do_work(self):
        self.pid = PID(P=0.8, I=0.1, D=0.1, point=45.0, below=-0.5, above=0.5)
        self.pid.set(10)
        # self.pid.
        print("PID started")


def pidtest():
    p = PIDWrapper()
    p.start()
    for i in range(10):
        p.update(i)

        print(p.get())


pidtest()