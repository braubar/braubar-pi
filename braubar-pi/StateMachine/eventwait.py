import threading
import time
import logging


class WaitFor:
    logging.basicConfig(level=logging.DEBUG,
                        format='(%(threadName)-9s) %(message)s', )

    e = threading.Event()

    def wait_for_event_timeout(self, e, t):
        while not e.isSet():
            logging.debug('wait_for_event_timeout starting')
            event_is_set = e.wait(t)
            logging.debug('event set: %s', event_is_set)
            if event_is_set:
                logging.debug('processing event')
            else:
                logging.debug('doing other things')

    def run(self):
        t2 = threading.Thread(name='non-blocking',
                              target=self.wait_for_event_timeout,
                              args=(self.e, 10))
        t2.start()
        logging.debug("started threads")
        return True

    def end(self):
        self.e.set()
