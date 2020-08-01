from typing import List, Callable


# TODO Add tiers in one achievements
# TODO Untested
class Achievement:
	def __init__(self, stats, name, desc, condition: Callable[[], bool], events: List, xp, hidden=False):
		from .stats import Stats
		self.stats: Stats = stats
		self.name: str = name
		self.desc: str = desc
		self.condition = condition
		self.xp: int = xp
		self.hidden = hidden
		self.got: bool = False
		for stat in events:
			stat.events.append(self)

	def check(self) -> None:
		if self.condition():
			self.got = True
			print("Got achieve" + repr(self))

	def __repr__(self):
		return f'<Achievement: {self.name=}, {self.got=}>'

	@staticmethod
	def basic(stats, name, desc: str, event, count, xp, hidden=False) -> 'Achievement':
		return Achievement(stats, name, desc.replace("{}", str(count)), lambda: event.value >= count, [event], xp, hidden)
