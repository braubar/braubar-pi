import sys

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
STATE_TEMP = 68.0

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

    def run(self):
        last_value = 0.0
        while True:
            temp = subprocess.check_output(["tail", "-1", "/tmp/braubar.temp"], universal_newlines=True)
            try:
                x = float(temp)
            except ValueError:
                try:
                    x = last_value
                except ValueError:
                    x = 0.0

            output = self.pid.step(dt=2.0, input=x)
            self.temp_actor(output, x)
            print("temp", x, "outout", output)
            time.sleep(2)
            last_value = float(x)

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


if __name__ == "__main__":

    try:
        brew_daemon = BrewDaemon()
        brew_daemon.run()

    finally:
        brew_daemon.powerstrip.all_off()
        brew_daemon.powerstrip.logout()
