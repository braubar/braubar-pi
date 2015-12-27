from queue import Queue
from threading import Event, Thread


class TempControl:
    num_worker_threads = 1
    q = None
    tempEvent = Event()




    def __init__(self):
        print("initialised")
        self.q = Queue()

    def worker(self):
        while True:
            item = self.q.get()
            if item is None:
                break
            # do_work(item)
            self.q.task_done()

    def runQueue(self):
        threads = []
        for i in range(self.num_worker_threads):
            t = Thread(target=self.worker)
            t.start()
            threads.append(t)

    def addItem(self, item):
        self.q.put(item)

        # for item in source():
        #     q.put(item)

        # block until all tasks are done
        # q.join()

        # stop workers
        # for i in range(num_worker_threads):
        #     q.put(None)
        # for t in threads:
        #     t.join()
