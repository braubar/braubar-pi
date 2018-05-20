# -*- coding: utf-8 -*-
import json
import os
import logging
import signal
import time

from datetime import datetime
from service.brewtimer import BrewTimer
from service.simplestate import SimpleState
from service.beginnerspid import BeginnersPID as Pid
from service.powerstrip import PowerStrip
from service.brewlog import BrewLog
from service.brewconfig import BrewConfig
from service.heatservice import HeatService
from service.ipchelper import IPCReceiver, TYPE_TEMP, TYPE_CONTROL, CONTROL_NEXT, CONTROL_PREV
from service.ipchelper import ipc
WAIT_THREAD_TIMEOUT = 0.05
WAIT_THREAD_NAME = "Thread_wait_temp"
HOST_IP = '0.0.0.0'
SENSOR_PORT = 50505
TEMP_TOLERANCE = 0.75
NEXT_STATE_FILE = "../data/next_state.brew"
LOG_BASE = "../log/brewlog_"
TEMP_RAW_FILE = "../data/temp.brew"
FLASK_FILE = "../braubar/flask_app.py"
SENSOR_SERVER_FILE = "../braubar/service/localtemp.py"

logfile = LOG_BASE + time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime()) + ".log"
brew_log = BrewLog()


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
    receiver = None
    brew_start = None

    def __init__(self):
        self.config = BrewConfig()
        self.powerstrip = PowerStrip(self.config.get("powerstrip")["url"])
        self.powerstrip.all_off()
        self.heatservice = HeatService()
        self.simplestate = SimpleState()
        self.init_pid()
        self.receiver = IPCReceiver(BrewConfig.BRAUBAR_QUEUE)
        print("opened message queue: ", self.receiver.name)

        signal.signal(signal.SIGALRM, self.msg_handler)

    def init_pid(self):
        self.pid = Pid(BrewConfig.P, BrewConfig.I, BrewConfig.D)
        self.pid.set_setpoint(0.0)
        self.pid.set_sample_time(1000.0)
        self.pid.set_output_limits(BrewConfig.MIN, BrewConfig.MAX)

    def msg_handler(self, a, b):
        # TODO: was war hier eigentlich gedacht? evtl. event zeugs?
        print("========= got message", a, b)

    def run(self, brew_id):
        print("running brew job:", brew_id)
        self.brew_id = brew_id
        self.state_params = self.simplestate.start()
        self.pid.set_setpoint(self.state_params["temp"])
        self.brew_start = datetime.now().isoformat()

        old_calculation_time = None
        try:
            while True:
                try:
                    msg_type, msg = self.receiver.receive()
                    print("msg_type: ", msg_type)
                    print("msg: ", msg)
                    if msg_type == TYPE_TEMP:
                        self.process_temp(msg, old_calculation_time)
                    elif msg_type == TYPE_CONTROL:
                        self.control_actions(msg)
                except ipc.ExistentialError:
                    self.receiver.close()
                    return False
                except ipc.BusyError as e:
                    print("socket busy:", e)
                    self.receiver.close()
                    return False
                except Exception as e:
                    print("brewdaemon-run: ", e)
        finally:
            self.receiver.cleanup()

    def process_temp(self, msg, old_calculation_time):
        # TODO sollte vielleicht als eigener thread laufen..
        # oder mit einer fifo queue.... damit nix schief geht. ipc pufert ja auch schon

        temp_current, sensor_id = self.convert_temp(msg)

        # computes timedelta for pid
        calculation_time = int(round(time.time() * 1000))
        if old_calculation_time:
            self.pid.set_sample_time(calculation_time - old_calculation_time)
        old_calculation_time = calculation_time

        # calculates PID output value
        output = self.pid.compute(temp_current)

        # switches powerstrip based on output value
        self.heatservice.temp_actor(output)

        logging.info(
            {"temp_actual": temp_current, "change": output, "state": self.state_params,
             "sensor": sensor_id})

        timer_passed_checked = 0.0
        if self.brew_timer is not None:
            timer_passed_checked = self.brew_timer.passed()
            brew_log.log(temp_current, self.state_params["temp"], output, sensor_id, self.simplestate.state,
                         self.brew_id, self.brew_start, int(self.brew_timer.passed()))
        else:
            brew_log.log(temp_current, self.state_params["temp"], output, sensor_id, self.simplestate.state,
                         self.brew_id, self.brew_start)

        print("temp_current", temp_current, "outout", output, "state_temp", self.state_params["temp"],
              "timer_passed", timer_passed_checked)

        if self.state_params["auto"] is True and self.state_params[
            "temp"] - TEMP_TOLERANCE <= temp_current:
            if self.brew_timer is None:
                print("Start BrewTimer for ", self.simplestate.state, "and", self.state_params["time"],
                      "seconds")
                self.brew_timer = BrewTimer(self.state_params["time"], self.next_state)
                self.brew_timer.start()

    def control_actions(self, command):
        if command["control"] == CONTROL_NEXT:
            if self.brew_timer:
                self.brew_timer.cancel()
            self.next_state()
        elif command["control"] == CONTROL_PREV:
            # TODO needs to be implemented
            pass

    def next_state(self):
        self.state_params = self.simplestate.next()
        if self.state_params["temp"] == 0.0:
            self.pid.set_mode(Pid.MANUAL)
        else:
            self.pid.set_mode(Pid.AUTOMATIC)
        self.pid.set_setpoint(self.state_params["temp"])
        self.brew_timer = None

    def prev_state(self):
        self.state_params = self.simplestate.prev()
        if self.state_params["temp"] == 0.0:
            self.pid.set_mode(Pid.MANUAL)
        else:
            self.pid.set_mode(Pid.AUTOMATIC)
        self.pid.set_setpoint(self.state_params["temp"])
        self.brew_timer = None

    def convert_temp(self, temp_json):
        sensor_id = -1
        temp_response = json.loads(temp_json)
        try:
            sensor_id = temp_response["id"]
            temp = float(temp_response["temp"])
        except ValueError:
            temp = 0.0
            print("Could not get correct temperature value")
        return temp, sensor_id

    def shutdown(self):
        self.powerstrip.all_off()
        self.powerstrip.logout()


if __name__ == "__main__":
    import atexit
    import argparse

    brew_daemon = BrewDaemon()

    parser = argparse.ArgumentParser(description="BrauBar daemon at your service.")
    parser.add_argument('--host', help="IP-Address to listen on. Default is 0.0.0.0", default="0.0.0.0")
    parser.add_argument('--id', help="Brau ID ", default="0")
    args = parser.parse_args()

    atexit.register(os.killpg, 0, signal.SIGTERM)
    atexit.register(brew_daemon.shutdown)

    os.setpgrp()

    HOST_IP = args.host

    brew_daemon.run(args.id)

    print("bye")
