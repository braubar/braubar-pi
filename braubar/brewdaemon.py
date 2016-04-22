# -*- coding: utf-8 -*-

import os
import logging
import signal
import time
import subprocess

from service.brewtimer import BrewTimer
from service.simplestate import SimpleState
# from libs.PIDs import Pid
from service.beginnerspid import BeginnersPID as Pid
from service.powerstrip import PowerStrip
from service.brewlog import BrewLog
from service.brewconfig import BrewConfig
from service.heatservice import HeatService

WAIT_THREAD_TIMEOUT = 0.05
WAIT_THREAD_NAME = "Thread_wait_temp"
HOST_IP = '0.0.0.0'
SENSOR_PORT = 50505
TEMP_TOLERANCE = 0.0
NEXT_STATE_FILE = "../data/next_state.brew"
LOG_BASE = "../log/brewlog_"
TEMP_RAW_FILE = "../data/temp.brew"
FLASK_FILE = "../braubar/flask_app.py"
SENSOR_SERVER_FILE = "../braubar/service/sensorserver.py"

logfile = LOG_BASE + time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime()) + ".log"
log = BrewLog()


class BrewDaemon:
    pid = None
    temp_control = None
    read_temp_socket = None
    temp_event = None
    brew_timer = None
    brew_id = None
    chart_service = None
    config = None
    heatservice = None
    state_params = None

    def __init__(self):
        self.config = BrewConfig()
        self.powerstrip = PowerStrip(self.config.get("powerstrip")["url"])
        self.powerstrip.all_off()
        self.heatservice = HeatService()
        self.simplestate = SimpleState()
        self.brew_id = int(round(time.time() * 1000))
        self.init_pid()

    def init_pid(self):
        self.pid = Pid(BrewConfig.P, BrewConfig.I, BrewConfig.D)
        self.pid.set_setpoint(0.0)
        self.pid.set_sample_time(2000.0)
        self.pid.set_output_limits(BrewConfig.MIN, BrewConfig.MAX)

    def run(self):
        last_value = 0.0

        self.state_params = self.simplestate.start()
        self.pid.set_setpoint(self.state_params["temp"])

        while True:
            temp_raw = subprocess.check_output(["tail", "-1", TEMP_RAW_FILE], universal_newlines=True)

            temp_current, last_value, sensor_id = self.convert_temp(temp_raw, last_value)

            # calculates PID output value
            output = self.pid.compute(temp_current)
            # switches plugstripe based on output value
            self.heatservice.temp_actor(output)

            logging.warning(
                {"temp_actual": temp_current, "change": output, "state": self.state_params, "sensor": sensor_id})

            timer_passed_checked = 0.0
            if self.brew_timer is not None:
                timer_passed_checked = self.brew_timer.passed()
                log.log(temp_current, self.state_params["temp"], output, sensor_id, self.simplestate.state,
                        self.brew_id, int(self.brew_timer.passed()))
            else:
                log.log(temp_current, self.state_params["temp"], output, sensor_id, self.simplestate.state,
                        self.brew_id)

            print("temp_current", temp_current, "outout", output, "state_temp", self.state_params["temp"],
                  "timer_passed", timer_passed_checked)

            time.sleep(2)
            last_value = float(temp_current)
            if not self.state_params["auto"] == True:
                if self.check_for_next():
                    self.next_state()
            elif self.state_params[
                "temp"] - TEMP_TOLERANCE <= temp_current:  # <= self.state_params["temp"] + TEMP_TOLERANCE:
                if self.brew_timer is None:
                    print("Start BrewTimer for ", self.simplestate.state, "and", self.state_params["time"], "seconds")
                    self.brew_timer = BrewTimer(self.state_params["time"], self.next_state)
                    self.brew_timer.start()

    def next_state(self):
        self.state_params = self.simplestate.next()
        if self.state_params["temp"] == 0.0:
            self.pid.set_mode(Pid.MANUAL)
        else:
            self.pid.set_mode(Pid.AUTOMATIC)
        self.pid.set_setpoint(self.state_params["temp"])
        self.brew_timer = None

    def convert_temp(self, temp_raw, last_value):
        sensor_id = -1
        try:
            sensor_id = int(temp_raw.split(":")[0])
            temp = float(temp_raw.split(":")[1])
        except ValueError:
            temp = 0.0
            print("Could not get correct temperature value")
        return temp, last_value, sensor_id

    def check_for_next(self):
        n = False
        try:
            next_raw = subprocess.check_output(["tail", "-1", NEXT_STATE_FILE], universal_newlines=True)
            n = next_raw.strip() == "True"
            print("FILE CHECK", next_raw.strip(), n)
            if n:
                os.system("echo '' > " + NEXT_STATE_FILE)
        finally:
            pass
        return n

    def start_flask(self, host=HOST_IP, brew_id=None):
        args = ["python3", FLASK_FILE, "--host", host]
        if brew_id:
            args.append("--id")
            args.append(str(brew_id))
        subprocess.Popen(args)

    def start_receive_temp(self, host=HOST_IP, port=None):
        args = ["python3", SENSOR_SERVER_FILE, host, str(port)]
        subprocess.Popen(args)

    def assureComFileExists(self):
        f = open(NEXT_STATE_FILE, 'w')
        f.close()
        f = open(TEMP_RAW_FILE, 'w')
        f.close()

    def shutdown(self):
        self.powerstrip.all_off()
        self.powerstrip.logout()


if __name__ == "__main__":
    import atexit
    import argparse

    brew_daemon = BrewDaemon()

    parser = argparse.ArgumentParser(description="BrauBar daemon at your service.")
    parser.add_argument('--host', help="IP-Address to listen on. Default is 0.0.0.0", default="0.0.0.0")
    args = parser.parse_args()

    atexit.register(os.killpg, 0, signal.SIGTERM)
    atexit.register(brew_daemon.shutdown)

    os.setpgrp()

    HOST_IP = args.host

    try:
        brew_daemon.start_receive_temp(host=HOST_IP, port=SENSOR_PORT)
        brew_daemon.assureComFileExists()
        brew_daemon.start_flask(host=HOST_IP, brew_id=brew_daemon.brew_id)
        brew_daemon.run()
    except KeyboardInterrupt:
        print("BrewDaemon is shutting down ...")
    finally:
        brew_daemon.shutdown()
        # os.killpg(0, signal.SIGTERM)
    print("bye")
