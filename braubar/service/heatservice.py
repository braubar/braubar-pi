from service.powerstrip import PowerStrip
from service.brewtimer import BrewTimer
from service.brewconfig import BrewConfig


class HeatService:

    bt = None
    DEFAULT_TIME = 10.0

    def temp_actor(self, pid_output):
        """
        switches the lan powerstrip on pid_output, if greater 0 switch PLUG_1 ON else switch OFF
        :param pid_output: PID calculated output value
        """


        status = PowerStrip().fetch_status()
        if pid_output > 0.0 and status.get(PowerStrip.PLUG_1) == PowerStrip.OFF:
            actor = HeatService.DEFAULT_TIME * (pid_output / BrewConfig.MAX)
            print("powerstrip on ", pid_output, "for", actor, "sec.")
            if self.alive():
                pass
            else:
                self.start(actor)
        if pid_output <= 0.0 and status.get(PowerStrip.PLUG_1) == PowerStrip.ON:
            if self.alive():
                self.stop()
                print("stopped timer")
            else:
                self.switch(PowerStrip.OFF)

    def start(self, duration):
        if duration == HeatService.DEFAULT_TIME:
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
