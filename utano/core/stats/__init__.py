import json
from datetime import datetime

from . import consts
from .achievement import Achievement
from .lvl import Lvl


class Stats:
	events = consts
	values = {}
	__song_songs = "Skip {} songs."
	achieve = [
		Achievement("Wait, what? Achievements?!", "Start program.", consts.program_started, 1, 0),
		Achievement("Getting hooked?", "Start program {} times.", consts.program_started, 25, 5),
		Achievement("Did you consider to support the developer?", "Start program {} times.", consts.program_started, 50, 10),

		Achievement("Hm, not this one.", __song_songs, events.song_skipped, 10, 5),
		Achievement("You should modify your playlist.", __song_songs, events.song_skipped, 25, 10),
		Achievement("Where is my song!?!", __song_songs, events.song_skipped, 100, 15),
		Achievement("Do you know this program have search bar, right?", __song_songs, events.song_skipped, 500, 20),

		Achievement("Hm, this one.", "Select {} songs from search menu", events.song_selected, 5, 5),
		Achievement("Master of choice.", "Select {} songs from search menu", events.song_selected, 25, 10),

		Achievement("Wait!", "Pause song {} times", events.paused, 5, 5),
		Achievement("Toilet break.", "Pause song {} times", events.paused, 25, 10),

		Achievement("One average song.", "Listen at least 3 minutes", events.total_time, 3 * 60, 5),
		Achievement("One hour.", "Listen at least 1 hour", events.total_time, 60 * 60, 10),
		Achievement("Ten hour version?", "Listen at least 10 hours", events.total_time, 60 * 60 * 10, 15),
		Achievement("Well spent day.", "Listen at least 1 day", events.total_time, 60 * 60 * 24, 20),

		Achievement("How was that melody again?", "Replay {} songs", events.song_replayed, 5, 5),
		Achievement("That's my jam!", "Replay {} songs", events.song_replayed, 25, 10),

		Achievement("Is this the end?", "Complete your playlist", events.playlist_completed, 1, 10),

		Achievement("IT'S OVER ONE HUNDRED !!! Wait, never mind.", "h_Try to set volume over 100", events.h_volume_max, 1, 10),
		Achievement("Long playlist", "h_Have over 100 songs in playlist", events.h_playlist_count, 1, 0)
	]

	def __init__(self, config: dict):
		self.config: dict = config
		self._achieve_got_call: callable = print
		self.values: dict = self._load()
		[x.check(self.values) for x in self.achieve]

	def set_callback(self, popup):
		self._achieve_got_call = popup
		self.values['lvl'].popup = print  # TODO Custom popup

	def set(self, event, count):
		if not event:
			return
		self.values[event.name] = count
		[x.check(self.values, self._achieve_got_call) for x in self.achieve if not x.got_it and x.event == event.name]

	def add(self, event, count=1):
		if not (event and count):
			return
		if event.name not in self.values:
			self.values[event.name] = count
		else:
			self.values[event.name] += count
		self.values['lvl'].exp += event.xp
		[x.check(self.values, self._achieve_got_call) for x in self.achieve if not x.got_it and x.event == event.name]

	def _load(self):
		c = {}
		try:
			with open(self.config['stats_path'], 'r') as f:
				c = json.load(f)
		except Exception as e:
			print(e)
		if not c:
			c[consts.stats_created.name] = datetime.now().strftime("%Y-%m-%d %H:%M")
		c['lvl'] = Lvl().load(c.get('lvl', {}))
		return c

	def save(self):
		self.values['lvl'] = self.values['lvl'].save()
		with open(self.config['stats_path'], 'w') as f:
			json.dump(self.values, f, indent=1)
