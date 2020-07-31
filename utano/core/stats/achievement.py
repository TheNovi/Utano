from typing import List


# TODO Add tiers in one achievements
# TODO Untested
class Achievement:
	def __init__(self, stats, name, desc, events: List, xp):
		from .stats import Stats
		self.stats: Stats = stats
		self.name: str = name
		self.desc: str = desc
		self.xp: int = xp
		self.got: bool = False
		for stat in events:
			stat.events.append(self)

	def check(self) -> None:
		if self.stats.song_played.value > 10:
			self.got = True
			print("Got achieve" + repr(self))

	def __repr__(self):
		return f'<Achievement: {self.name=}, {self.got=}>'
