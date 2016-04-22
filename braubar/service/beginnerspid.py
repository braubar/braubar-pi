import time


class BeginnersPID:
    """
    A PID implementation borrowed by: http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/

    """
    AUTOMATIC = True
    MANUAL = False

    last_time = int(round(time.time() * 1000))
    pid_input = 0.0
    output = 0.0
    setpoint = 0.0
    i_term = 0.0
    last_input = 0.0
    kp = None
    ki = None
    kd = None
    sample_time = 1000  # in milliseconds
    out_min = None
    out_max = None
    in_auto = False

    def __init__(self, kp, ki, kd, o_min=-100, o_max=100):
        self.set_tunings(kp, ki, kd)
        self.set_output_limits(o_min, o_max)

    def compute(self, pid_input):
        if not self.in_auto:
            return 0.0
        self.pid_input = pid_input

        # time since last calculation
        now = int(round(time.time() * 1000))
        time_change = now - self.last_time
        if time_change >= self.sample_time:
            # calculating error variables
            error = self.setpoint - self.pid_input
            self.i_term += (self.ki * error)
            if self.i_term > self.out_max:
                self.i_term = self.out_max
            elif self.i_term < self.out_min:
                self.i_term = self.out_min
            d_input = (pid_input - self.last_input)

            # compute PID output
            self.output = self.kp * error + self.i_term - self.kd * d_input
            if self.output > self.out_max:
                self.output = self.out_max
            elif self.output < self.out_min:
                self.output = self.out_min

            # save values for next computation
            self.last_input = pid_input
            self.last_time = now
        return self.output

    def set_tunings(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def set_sample_time(self, new_sample_time):
        if new_sample_time > 0:
            ratio = new_sample_time / self.sample_time
            self.ki *= ratio
            self.kd /= ratio
            self.sample_time = abs(new_sample_time)

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def set_output_limits(self, o_min, o_max):
        if o_min > o_max:
            pass

        self.out_min = o_min
        self.out_max = o_max

        if self.output > self.out_max:
            self.output = self.out_max
        elif self.output < self.out_min:
            self.output = self.out_min

        if self.i_term > self.out_max:
            self.i_term = self.out_max
        elif self.i_term < self.out_min:
            self.i_term = self.out_min

    def set_mode(self, mode):
        new_auto = mode == self.AUTOMATIC
        if new_auto and not self.in_auto:
            self.initialize()
        self.in_auto = new_auto

    def initialize(self):
        self.last_input = self.pid_input
        self.i_term = self.output
        if self.i_term > self.out_max:
            self.i_term = self.out_max
        elif self.i_term < self.out_max:
            self.i_term = self.out_min