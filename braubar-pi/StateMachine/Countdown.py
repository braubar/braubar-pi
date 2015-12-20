import time
import threading
from datetime import timedelta


class Countdown:
    delta = 0

    def hello(self):
        print("hello, world")

    def wait_with_status(self,delay, status_delay=1):

        wait_to = time.time() + delay
        while wait_to > time.time():
            self.delta = wait_to - time.time()
            print(self.delta, " sec to wait... ")
            time.sleep(status_delay)
        self.delta = 0


def test():
    c = Countdown()
    d = timedelta(seconds=10)
    t = threading.Thread(target=c.wait_with_status,args=[d.seconds])
    t.start()

    # c.wait_with_status(d)
    while t.is_alive():
        time.sleep(1)
        print(c.delta)

# test()
