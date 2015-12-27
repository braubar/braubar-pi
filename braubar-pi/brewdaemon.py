import sys

from simplestate import SimpleState

sys.path.append('./libs')
sys.path.append('./helper')
sys.path.append('./service')

import subprocess
from PIDs import Pid
from powerstrip import PowerStrip
import logging
import time

from readsocket import ReadSocket
from threading import Event, Thread, Timer
import os
from brewtimer import BrewTimer

P = 8000.0
I = 0.0
D = 350000.0
MIN = -5.0
MAX = 5.0
WAIT_THREAD_TIMEOUT = 0.05
WAIT_THREAD_NAME = "Thread_wait_temp"
SOCKET_IP = '192.168.2.9'
SOCKET_PORT = 10001
STATE_TEMP = 45.0

logfile = "log/brewlog_" + time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime()) + ".log"
logging.basicConfig(filename=logfile, level=logging.WARN, format='[BrewData] %(asctime)s %(message)s')


class BrewDaemon:
    pid = None
    temp_control = None
    read_temp_socket = None
    temp_event = None

    def __init__(self):

        self.pid = Pid(P, I, D)
        self.pid.range(MIN, MAX)
        self.pid.set(STATE_TEMP)
        self.powerstrip = PowerStrip()
        self.simplestate = SimpleState()

    def run(self):
        last_value = 0.0

        self.simplestate.start()

        while True:
            temp_raw = subprocess.check_output(["tail", "-1", "/tmp/braubar.temp"], universal_newlines=True)
            temp_current, last_value = self.convert_temp(temp_raw, last_value)

            # calculates PID output value
            output = self.pid.step(dt=2.0, input=temp_current)

            # switches plugstripe based on output value
            self.temp_actor(output, temp_current)

            print("temp", temp_current, "outout", output)

            time.sleep(2)
            last_value = float(temp_current)

    def convert_temp(self, temp_raw, last_value):
        try:
            temp = float(temp_raw)
        except ValueError:
            try:
                temp = last_value
            except ValueError:
                temp = 0.0
        return (temp, last_value)

    def temp_actor(self, pid_output, x):
        self.last_switch = PowerStrip.OFF
        status = self.powerstrip.fetch_status()
        if pid_output > 0 and status.get(PowerStrip.PLUG_1) == PowerStrip.OFF:
            self.last_switch == PowerStrip.ON
            print("powerstrip on ", pid_output)
            PowerStrip().switch(PowerStrip.PLUG_1, PowerStrip.ON)
        if pid_output < 0 and status.get(PowerStrip.PLUG_1) == PowerStrip.ON:
            self.last_switch == PowerStrip.OFF
            print("powerstrip on ", pid_output)
            PowerStrip().switch(PowerStrip.PLUG_1, PowerStrip.OFF)

        logging.warning([time.time(), x, pid_output])

    def shutdown(self):
        self.powerstrip.all_off()
        self.powerstrip.logout()


if __name__ == "__main__":

    try:
        brew_daemon = BrewDaemon()
        brew_daemon.run()
    except KeyboardInterrupt:
        print("BrewDaemon is shutting down ...")
    finally:
        brew_daemon.shutdown()
    print("bye")
