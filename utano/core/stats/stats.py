import json
from datetime import datetime
from json.decoder import JSONDecodeError
from os.path import exists as path_exists
from typing import List

from core.stats import Achievement


# TODO Lvl
# TODO Test all stats
# TODO Dynamic stat (lambda as value (no add/set))
class Stats:
	class Stat:
		def __init__(self, xp: int = 0):
			self.xp: int = xp
			self.__value: int = 0
			self.events: List = []

		@property
		def value(self):
			return self.__value

		def __trigger_events(self):
			[e.check() for e in self.events if not e.got]

		def add(self, value: int = 1):
			self.__value += value
			self.__trigger_events()

		def set(self, value):
			self.__value = value
			self.__trigger_events()

	def __init__(self, conf):
		self.stats_created: Stats.Stat = Stats.Stat()
		self.program_started: Stats.Stat = Stats.Stat()
		self.song_played: Stats.Stat = Stats.Stat(3)
		self.song_skipped: Stats.Stat = Stats.Stat(1)
		self.paused: Stats.Stat = Stats.Stat()
		self.song_replayed: Stats.Stat = Stats.Stat(1)
		self.song_selected: Stats.Stat = Stats.Stat(2)
		self.playlist_completed: Stats.Stat = Stats.Stat(10)
		self.total_time: Stats.Stat = Stats.Stat()
		# self.songs_guessed_correctly: Stats.Stat = Stats.Stat(5) #NOSONAR TODO
		# self.songs_guessed_incorrectly: Stats.Stat = Stats.Stat(1)
		self.h_volume_max: Stats.Stat = Stats.Stat()
		self.h_playlist_count: Stats.Stat = Stats.Stat()

		__song_songs = "Skip {} songs."
		self.achievements: List[Achievement] = [
			Achievement("Wait, what? Achievements?!", "Start program.", self.program_started, group=1),
			Achievement("Getting hooked?", "Start program {} times.", self.program_started, count=25, xp=5, group=1),
			Achievement("Did you consider to support the developer?", "Start program {} times.", self.program_started, count=50, xp=10, group=1),

			Achievement("Hm, not this one.", __song_songs, self.song_skipped, count=10, xp=5, group=2),
			Achievement("You should modify your playlist.", __song_songs, self.song_skipped, count=25, xp=10, group=2),
			Achievement("Where is my song!?!", __song_songs, self.song_skipped, count=100, xp=15, group=2),
			Achievement("Do you know this program have search bar, right?", __song_songs, self.song_skipped, count=500, xp=20, group=2),

			Achievement("Hm, this one.", "Select {} songs from search menu", self.song_selected, count=5, xp=5, group=3),
			Achievement("Master of choice.", "Select {} songs from search menu", self.song_selected, count=25, xp=10, group=3),

			Achievement("Wait!", "Pause song {} times", self.paused, count=5, xp=5, group=4),
			Achievement("Toilet break.", "Pause song {} times", self.paused, count=25, xp=10, group=4),

			Achievement("One average song.", "Listen at least 3 minutes", self.total_time, count=3 * 60, xp=5, group=5),
			Achievement("One hour.", "Listen at least 1 hour", self.total_time, count=60 * 60, xp=10, group=5),
			Achievement("Ten hour version?", "Listen at least 10 hours", self.total_time, count=60 * 60 * 10, xp=15, group=5),
			Achievement("Well spent day.", "Listen at least 1 day", self.total_time, count=60 * 60 * 24, xp=20, group=5),

			Achievement("How was that melody again?", "Replay {} songs", self.song_replayed, count=5, xp=5, group=6),
			Achievement("That's my jam!", "Replay {} songs", self.song_replayed, count=25, xp=10, group=6),

			Achievement("Is this the end?", "Complete your playlist", self.playlist_completed, xp=10),

			Achievement("IT'S OVER ONE HUNDRED !!! Wait, never mind.", "Try to set volume over 100", self.h_volume_max, xp=10, hidden=True),
			Achievement("Long playlist", "Have over 100 songs in playlist", self.h_playlist_count, hidden=True)
		]

		self.conf = conf
		self.load()

		if self.stats_created.value == 0:
			self.stats_created.set(datetime.now().strftime("%Y-%m-%d %H:%M"))

	def load(self):
		if path_exists(self.conf.stats_path):
			try:
				with open(self.conf.stats_path) as f:
					d: dict = json.load(f)
			except JSONDecodeError:
				print("Can't load stats")
				return
			self.stats_created.set(d.get('stats_created', 0))
			self.program_started.set(d.get('program_started', 0))
			self.song_played.set(d.get('song_played', 0))
			self.song_skipped.set(d.get('song_skipped', 0))
			self.paused.set(d.get('paused', 0))
			self.song_replayed.set(d.get('song_replayed', 0))
			self.song_selected.set(d.get('song_selected', 0))
			self.playlist_completed.set(d.get('playlist_completed', 0))
			self.total_time.set(d.get('total_time', 0))
			self.h_volume_max.set(d.get('h_volume_max', 0))
			self.h_playlist_count.set(d.get('h_playlist_count', 0))

	def save(self):
		with open(self.conf.stats_path, 'w') as f:
			json.dump({
				'stats_created': self.stats_created.value,
				'program_started': self.program_started.value,
				'song_played': self.song_played.value,
				'song_skipped': self.song_skipped.value,
				'paused': self.paused.value,
				'song_replayed': self.song_replayed.value,
				'song_selected': self.song_selected.value,
				'playlist_completed': self.playlist_completed.value,
				'total_time': self.total_time.value,
				'h_volume_max': self.h_volume_max.value,
				'h_playlist_count': self.h_playlist_count.value
			}, f, indent=True)
