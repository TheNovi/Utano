class Achievement:
	def __init__(self, name: str, desc: str, event, count: int, xp: int):
		self.name: str = name
		self.desc: str = desc.replace("{}", str(count))
		self.event = event
		self.count: int = count
		self.xp: int = xp
		self.got_it = False

	def check(self, stat, popup=None):
		if (not self.got_it) and self.event.name in stat and stat[self.event.name] >= self.count:
			self.got_it = True
			if popup:
				popup(self)
