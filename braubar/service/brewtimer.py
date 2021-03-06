from threading import Timer
from datetime import datetime


class BrewTimer:
    start_time = None
    timer = None
    duration = None

    def __init__(self, duration, function):
        """
        Call a function after a specified duration
        :param duration: duration in seconds
        :param function: called after "duration" seconds
        :return: instance of BrewTimer
        """
        self.duration = duration
        self.timer = Timer(self.duration, function)

    def start(self):
        self.start_time = datetime.now()
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

    def alive(self):
        return self.timer.is_alive()

    def passed(self):
        if self.start_time:
            return (datetime.now() - self.start_time).total_seconds()
        return 0

    def remaining(self):
        return self.duration - self.passed()

    def percentage(self):
        return int((self.passed() / self.duration) * 100)
