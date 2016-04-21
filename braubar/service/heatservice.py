from powerstrip import PowerStrip
from brewtimer import BrewTimer
from brewconfig import BrewConfig


class HeatService:

    bt = None

    def temp_actor(self, pid_output):
        """
        switches the lan powerstrip on pid_output, if greater 0 switch PLUG_1 ON else switch OFF
        :param pid_output: PID calculated output value
        """
        status = PowerStrip().fetch_status()
        if pid_output > 0.1 and status.get(PowerStrip.PLUG_1) == PowerStrip.OFF:
            print("powerstrip on ", pid_output, "for", pid_output, "sec.")
            if self.alive():
                pass
            else:
                self.start(pid_output)
        if pid_output < 0 and status.get(PowerStrip.PLUG_1) == PowerStrip.ON:
            if self.alive():
                self.stop()
            else:
                self.switch(PowerStrip.OFF)

    def start(self, duration):
        if duration == BrewConfig.MAX:
            self.bt = BrewTimer(duration, self.alive)
        else:
            self.bt = BrewTimer(duration, self.switch)
        self.switch(PowerStrip.ON)
        self.bt.start()

    def stop(self):
        self.bt.cancel()
        self.switch(PowerStrip.OFF)

    def switch(self, state=0):
        status = PowerStrip().switch(PowerStrip.PLUG_1, state)
        return status

    def alive(self):
        if self.bt:
            return self.bt.alive()
        return False

    def remaining(self):
        if self.bt:
            return self.bt.remaining()
        return False
