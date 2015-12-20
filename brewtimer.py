from threading import Timer
from datetime import datetime

class BrewTimer:
	start_time = None
	timer = None
	duration = None

	def __init__(self, duration, function):
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
		return (datetime.now() - self.start_time).total_seconds()

	def remaining(self):
		return self.duration - self.passed()

	def percentage(self):
		return int((self.passed() / self.duration) * 100)
