# TODO Add tiers in one achievements
# TODO Untested
class Achievement:
	def __init__(self, name, desc: str, stat, /, *, count: int = 1, xp: int = 0, group: int = 0, hidden=False):
		self.name: str = name
		self.desc: str = desc.replace('{}', str(count))
		self.stat = stat
		self.count = count
		self.xp: int = xp
		self.group = group
		self.hidden = hidden
		self.got: bool = False
		stat.events.append(self)

	def check(self) -> None:
		self.got = self.stat.value >= self.count

	def __repr__(self):
		return f'<Achievement: {self.name=}, {self.got=}>'
