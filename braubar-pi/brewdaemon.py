import os
import logging
import time
import sys
sys.path.append('./libs')
sys.path.append('./StateMachine')
sys.path.append('./helper')
sys.path.append('./service')

from simplestate import SimpleState
import subprocess
from PIDs import Pid
from powerstrip import PowerStrip

P = 8000.0
I = 0.0
D = 350000.0
MIN = -5.0
MAX = 5.0
WAIT_THREAD_TIMEOUT = 0.05
WAIT_THREAD_NAME = "Thread_wait_temp"
SOCKET_IP = '192.168.2.9'
SOCKET_PORT = 10001

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
        self.pid.set(0.0)
        self.powerstrip = PowerStrip()
        self.simplestate = SimpleState()
        self.powerstrip.all_off()

    def run(self):
        last_value = 0.0

        state_params = self.simplestate.start()
        self.pid.set(state_params["temp"])

        while True:
            temp_raw = subprocess.check_output(["tail", "-1", "/tmp/braubar.temp"], universal_newlines=True)
            temp_current, last_value = self.convert_temp(temp_raw, last_value)

            # calculates PID output value
            output = self.pid.step(dt=2.0, input=temp_current)

            # switches plugstripe based on output value
            self.temp_actor(output, temp_current)

            print("temp_current", temp_current, "outout", output, "state_temp", state_params["temp"])

            time.sleep(2)
            last_value = float(temp_current)
            if not state_params["auto"] == 1:
                if self.check_for_next():
                    state_params = self.simplestate.next()
                    self.pid.set(state_params["temp"])


    def convert_temp(self, temp_raw, last_value):
        try:
            temp = float(temp_raw)
        except ValueError:
            try:
                temp = last_value
            except ValueError:
                temp = 0.0
        return (temp, last_value)

    def check_for_next(self):
        n = False
        try:
            next_raw = subprocess.check_output(["tail", "-1", "next_state.brew"], universal_newlines=True)
            n = bool(next_raw)
            if n:
                os.system("echo '' > next_state.brew")
        finally:
            pass
        return n

    def temp_actor(self, pid_output, temp_current):
        """
        switches the lan powerstripe on pid_output, if greater 0 switch PLUG_1 ON else switch OFF
        :param pid_output: PID calculated output value
        :param temp_current: current temperature from sensor
        :return:
        """
        status = self.powerstrip.fetch_status()
        if pid_output > 0 and status.get(PowerStrip.PLUG_1) == PowerStrip.OFF:
            print("powerstrip on ", pid_output)
            PowerStrip().switch(PowerStrip.PLUG_1, PowerStrip.ON)
        if pid_output < 0 and status.get(PowerStrip.PLUG_1) == PowerStrip.ON:
            print("powerstrip on ", pid_output)
            PowerStrip().switch(PowerStrip.PLUG_1, PowerStrip.OFF)

        logging.warning([time.time(), temp_current, pid_output])

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
