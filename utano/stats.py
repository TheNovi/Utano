import json
from datetime import datetime
from typing import Callable


class Achievement:
	def __init__(self, name, desc, key, count):
		self.name = name
		self.desc = desc.replace("{}", str(count))
		self.key = key
		self.count = count
		self.got_it = False

	def check(self, stat, popup=None):
		if stat[self.key] >= self.count and not self.got_it:
			self.got_it = True
			if popup:
				popup(self)


class Lvl:
	def __init__(self, lvl=1, exp=0, method=lambda lvl: 2 ** lvl, popup: Callable = None):
		self._lvl = lvl
		self._exp = exp
		self.method = method
		self.popup = popup

	@property
	def exp(self):
		return self._exp

	@exp.setter
	def exp(self, value):
		self._exp = max(0, value)
		self._check()

	@property
	def lvl(self):
		return self._lvl

	def _check(self):
		while self.exp_to_next_lvl() <= 0:
			self._exp -= self.total_exp_to_next_lvl()
			self._lvl += 1
			if self.popup:
				self.popup(self)

	def total_exp_to_next_lvl(self):
		return self.method(self.lvl)

	def exp_to_next_lvl(self):
		return self.total_exp_to_next_lvl() - self.exp

	def __repr__(self) -> str:
		return f"<Nlvl: lvl: {self.lvl}, exp: {self.exp}, total_next: {self.total_exp_to_next_lvl()}>"

	def save(self) -> dict:  # TODO Save method
		return {'l': self._lvl, 'e': self._exp}

	def load(self, d: dict):
		self._lvl = d.get('l', self._lvl)
		self._exp = d.get('e', self._exp)
		return self


class Stats:
	_stats = {
		'stats created': 0,
		'program started': 0,
		'song played': 3,
		'song skipped': 1,
		'paused': 0,
		'song replayed': 1,
		'song selected': 2,
		'playlist completed': 5,
		'total time': 0,

		'h_volume max': 0,
		'h_playlist count': 0
	}

	achievements = [  # Achievement("", "", '', 0),
		Achievement("Wait, what? Achievements?!", "Start program.", 'program started', 1),
		Achievement("Getting hooked?", "Start program {} times.", 'program started', 25),
		Achievement("Did you consider to support the developer?", "Start program {} times.", 'program started', 50),

		Achievement("Hm, not this one.", "Skip {} songs.", 'song skipped', 10),
		Achievement("You should modify your playlist.", "Skip {} songs.", 'song skipped', 25),
		Achievement("Where is my song!?!", "Skip {} songs.", 'song skipped', 100),
		Achievement("Do you know this program have search bar, right?", "Skip {} songs.", 'song skipped', 500),

		Achievement("Hm, this one.", "Select {} songs from search menu", 'song selected', 5),
		Achievement("Master of choice.", "Select {} songs from search menu", 'song selected', 25),

		Achievement("Wait!", "Pause song {} times", 'paused', 5),
		Achievement("Toilet break.", "Pause song {} times", 'paused', 25),

		Achievement("One average song.", "Listen at least 3 minutes", 'total time', 3 * 60),
		Achievement("One hour.", "Listen at least 1 hour", 'total time', 60 * 60),
		Achievement("Ten hour version?", "Listen at least 10 hours", 'total time', 60 * 60 * 10),
		Achievement("Well spent day.", "Listen at least 1 day", 'total time', 60 * 60 * 24),

		Achievement("How was that melody again?", "Replay {} songs", 'song replayed', 5),
		Achievement("That's my jam!", "Replay {} songs", 'song replayed', 25),

		Achievement("Is this the end?", "Complete your playlist", 'playlist completed', 1),

		Achievement("IT'S OVER ONE HUNDRED !!! Wait, never mind.", "h_Try to set volume over 100", 'h_volume max', 1),
		Achievement("Long playlist", "h_Have over 100 songs in playlist", 'h_playlist count', 1)
	]

	class CheatSheet:
		program_started = 'program started'
		song_played = 'song played'
		song_skipped = 'song skipped'
		paused = 'paused'
		song_replayed = 'song replayed'
		song_selected = 'song selected'
		playlist_completed = 'playlist completed'
		total_time = 'total time'

		h_volume_max = 'h_volume max'
		h_playlist_count = 'h_playlist count'

	def __init__(self, path):
		self.path = path
		self._achieve_got_call = print
		self.stats: dict = self._load()
		[x.check(self.stats) for x in Stats.achievements]

	def set_callback(self, popup):
		self._achieve_got_call = popup
		self.stats['lvl'].popup = print  # TODO Custom popup

	def set(self, key, count):
		if not key:
			return
		self.stats[key] = count
		[x.check(self.stats, self._achieve_got_call) for x in Stats.achievements if not x.got_it and x.key == key]

	def add(self, key, count=1):
		if not (key and count):
			return
		# print(key, count)
		self.stats[key] += count
		self.stats['lvl'].exp += self._stats[key]
		[x.check(self.stats, self._achieve_got_call) for x in Stats.achievements if not x.got_it and x.key == key]

	def _load(self):
		c = {}
		try:
			with open(self.path, 'r') as f:
				c = json.load(f)
		except Exception as e:
			print(e)
		if not c:
			c[Stats._stats[0][0]] = datetime.now().strftime("%Y-%m-%d %H:%M")
		for k in Stats._stats:
			if k not in c:
				c[k] = 0
		c['lvl'] = Lvl().load(c.get('lvl', {}))
		return c

	def save(self):
		self.stats['lvl'] = self.stats['lvl'].save()
		with open(self.path, 'w') as f:
			json.dump(self.stats, f, indent=1)
