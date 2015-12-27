
# pids - Generic proportional-integral-derivative controllers.

'''

Generic proportional-integral-derivative controllers.

ABSTRACT

    A proportional-integral-derivative controller (PID controller) is a
    generic control loop feedback mechanism widely used in industrial
    control systems.  A PID controller calculates an "error" value as the
    difference between a measured process variable and a desired
    setpoint. The controller attempts to minimize the error by adjusting
    the process control inputs.

    For instance, a sensor may return a voltage representing a
    thermocouple reading for an oven temperature, and an actuator may
    be sent a signal using completely different voltage scale to describe
    the amount of fuel to burn in the oven.  A PID controller can link
    the two systems as a thermostat:  add more fuel when the oven cools,
    reduce fuel when the oven is overly hot, closing in on a desired
    temperature.

SYNOPSIS

    >>> import pids

    >>> p = pids.Pid( Kproportional, Kintegral, Kderivative )
    >>> p.range( get_my_actuator_minimum(), get_my_actuator_maximum() )

    >>> while True:
    ...   output = p.step( my_clock.get_dt(), get_my_sensor_value() )
    ...   set_my_actuator_value( output )

    The tuning of the PID parameters is complicated, and depends
    on the design of the devices involved.  Experimentation is
    key.

    The meaning of the input, output and limit parameters are explained
    through a couple of simple example applications.

EXAMPLE APPLICATIONS

    A PID Controller is often selected to control a servomotor.

    Many common servomotors swing an arm through an arc, from a
    minimum position (e.g., -80 degrees) to a maximum (+80 degrees).
    The angle of the arm may be measured by eye in degrees, but
    electrically, this is sensed by an electrical resistance value
    (e.g., 100 Ohms to 1000 Ohms).

    The input signal is a pulse width modulated signal, with pulses
    between a minimum width (e.g., 1ms high out of every 20ms) and a
    maximum width (2ms high out of every 20ms).

    For the PID, this describes the units required for ranges and the
    set point.

    * the input is the measured angle (say, in ohms)
    * the set point is the desired angle (also in ohms)
    * the output is the pwm rate applied to motor (in milliseconds)


    Another purpose for a PID controller is as an oven thermostat.

    A measuring thermocouple is used to detect the current temperature
    in the oven.  It has a reading in electrical resistance (e.g., 10
    K Ohms at 300 degrees Celsius, and +100 Ohms per 10 degrees
    Celsius below that level).  Sensors may have a non-linear
    relationship but the curve is generally sufficiently smooth to
    work here.

    A heating coil is used to produce heat in the oven.  It is rated
    to produce heat with a known level of electrical current (e.g.,
    anywhere from 0 to 3 Amperes).  An actual coil may simply be "on"
    or "off," but by alternating the state, heat can be regulated more
    smoothly.  The output of the controller should decide the level of
    alternation requested (e.g., from 0 or always off, to 1 or always
    on).

    * The input is measured temperature (in ohms)
    * The set point is desired temperature (in ohms)
    * The output is the heating coil activation (from zero to one)

SEE ALSO

    http://en.wikipedia.org/wiki/PID_controller

'''


class Pid (object):

    '''A discrete PID (Proportional-Integral-Derivative) controller.'''

    def __init__(self, P=1.0, I=1.0, D=1.0, point=0.0, below=-1.0, above=1.0):
        '''Sets up basic operational parameters for the controller.
        Three constants for the "tuning" of the controller can be given.
          * P (proportional gain) scales acceleration to new setpoints
          * I (integral gain) scales correction of error buildup
          * D (derivative gain) scales bounded rate of output change
        The initial desired ouput value or "point" can be given.
        The overall output range ("below" and "above") can be given.
        '''
        self.tune(P, I, D)
        self.range(below, above)
        self.output = below
        self.set(point)
        self.input = self.measure()

    def reset(self):
        self._integral = 0.0
        self._previous = 0.0

    def step(self, dt=1.0, input=None):
        '''Update the controller with a new input, to get new output.
        The time step "dt" can be given, or is assumed as an arbitrary 1.0.
        If a new "input" value a callable object, it is called for a value.
        If a new "input" value is not given here, measure() is called.
        '''
        if input is None:
            self.input = self.measure()
        elif callable(input):
            self.input = input()
        else:
            self.input = input
        err = self.setpoint - self.input
        self._integral += err * dt
        I = self._integral
        D = (err - self._previous) / dt
        output = self.Kp*err + self.Ki*I + self.Kd*D
        self._previous = err
        self.output = self.bound(output)
        return  self.output

    def bound(self, output):
        '''Ensure the output falls within the current output range.
        May be overridden with a new method if overshoot is allowed.
        '''
        return max(min(output, self.maxout), self.minout)

    def range(self, below, above):
        '''Set the overall output range.
        Outputs are bounded to remain within this range with the bound()
        overridable method.
        '''
        if below > above:
            (above, below) = (below, above)
        self.minout = below
        self.maxout = above
        self.reset()

    def tune(self, P, I, D):
        '''Sets the three constant tuning parameters, P, I, and D.'''
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.reset()

    def set(self, point):
        '''Sets the desired output value to which the controller seeks.'''
        self.setpoint = point

    def get(self):
        '''Returns the current output value at any time.'''
        return self.output

    def measure(self):
        '''May be overridden to calculate a new input value.'''
        return 0.0

#----------------------------------------------------------------------------

if __name__ == '__main__':

    import interpolations

    def worm(terms, width=120):
        line = ' '*width
        for term in terms:
            left, x, right, sym = term
            h = int( interpolations.linear(left, right, x, 0, width-2) )
            line = line[:h] + sym + line[h+1:]
        print("|" + line + "|")

    class ServoPid (Pid):
        where = None
        def __init__(self, **config):
            self.speed = 1
            self.where = 0
            self.maxwhere = 90
            self.minwhere = -90
            super(ServoPid, self).__init__(**config)
        def measure(self):
            self.where += self.output / 3.0
            self.where = max(min(self.where, self.maxwhere), self.minwhere)
            return self.where

    import math
    import random

    pid = ServoPid()
    pid.range(-10.0, 10.0)
    pid.tune(100.8,.000001,.002)
    pid.set(10)
    for i in range(100):
        pid.step()
        #worm(pid.minout, pid.get(), pid.maxout)
        worm( [ (pid.minwhere, pid.setpoint, pid.maxwhere, '+'),
                (pid.minwhere, pid.where, pid.maxwhere, '*') ] )
        if random.random() < 0.10:
            pid.set(random.random() * 25 - 12)