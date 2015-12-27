import threading
import time
import logging


class WaitFor:
    logging.basicConfig(level=logging.DEBUG,
                        format='(%(threadName)-9s) %(message)s', )

    e = threading.Event()

    def wait_for_event_timeout(self, e, timeout=5):
        self.e = e
        while not e.isSet():
            logging.debug('wait_for_event_timeout starting')
            event_is_set = self.e.wait(timeout)
            logging.debug('event set: %s', event_is_set)
            if event_is_set:
                logging.debug('processing event')
                file = open("current.temp", mode='rt')
                file.readline(1)
                file.close()
            else:
                logging.debug('doing other things')

    def run(self):
        '''
        startet einen loop, der nicht blockierend auf das zurückgegebene event.set() wartet.
        :return: threading.Event wenn set() aufgerufen wird, läuft die Methode los
        '''
        t2 = threading.Thread(name='non-blocking',
                              target=self.wait_for_event_timeout,
                              args=(self.e, 10))
        t2.start()
        logging.debug("started threads")
        return self.e

    def end(self):
        self.e.set()
