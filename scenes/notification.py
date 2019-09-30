import tkinter
from datetime import datetime

from scenes.scene import Scene


# noinspection PyAttributeOutsideInit
class Notification(Scene):
	def _init_(self):
		self.time = 1
		self.timer = datetime.now()

	def activate(self, time: int = 5):
		self.time = time
		self.timer = datetime.now()
		super().activate()
		return self

	def tick(self):
		return (datetime.now() - self.timer).total_seconds() >= self.time
