import json
from datetime import datetime
from json.decoder import JSONDecodeError
from os.path import exists as path_exists
from typing import List

from core.stats import Achievement


# TODO Lvl
# TODO Test all stats
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
			Achievement.basic(self, "Wait, what? Achievements?!", "Start program.", self.program_started, 1, 0),
			Achievement.basic(self, "Getting hooked?", "Start program {} times.", self.program_started, 25, 5),
			Achievement.basic(self, "Did you consider to support the developer?", "Start program {} times.", self.program_started, 50, 10),

			Achievement.basic(self, "Hm, not this one.", __song_songs, self.song_skipped, 10, 5),
			Achievement.basic(self, "You should modify your playlist.", __song_songs, self.song_skipped, 25, 10),
			Achievement.basic(self, "Where is my song!?!", __song_songs, self.song_skipped, 100, 15),
			Achievement.basic(self, "Do you know this program have search bar, right?", __song_songs, self.song_skipped, 500, 20),

			Achievement.basic(self, "Hm, this one.", "Select {} songs from search menu", self.song_selected, 5, 5),
			Achievement.basic(self, "Master of choice.", "Select {} songs from search menu", self.song_selected, 25, 10),

			Achievement.basic(self, "Wait!", "Pause song {} times", self.paused, 5, 5),
			Achievement.basic(self, "Toilet break.", "Pause song {} times", self.paused, 25, 10),

			Achievement.basic(self, "One average song.", "Listen at least 3 minutes", self.total_time, 3 * 60, 5),
			Achievement.basic(self, "One hour.", "Listen at least 1 hour", self.total_time, 60 * 60, 10),
			Achievement.basic(self, "Ten hour version?", "Listen at least 10 hours", self.total_time, 60 * 60 * 10, 15),
			Achievement.basic(self, "Well spent day.", "Listen at least 1 day", self.total_time, 60 * 60 * 24, 20),

			Achievement.basic(self, "How was that melody again?", "Replay {} songs", self.song_replayed, 5, 5),
			Achievement.basic(self, "That's my jam!", "Replay {} songs", self.song_replayed, 25, 10),

			Achievement.basic(self, "Is this the end?", "Complete your playlist", self.playlist_completed, 1, 10),

			Achievement.basic(self, "IT'S OVER ONE HUNDRED !!! Wait, never mind.", "Try to set volume over 100", self.h_volume_max, 1, 10, hidden=True),
			Achievement.basic(self, "Long playlist", "Have over 100 songs in playlist", self.h_playlist_count, 1, 0, hidden=True)
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
				# 'songs_guessed_correctly': self.songs_guessed_correctly.value,
				# 'songs_guessed_incorrectly': self.songs_guessed_incorrectly.value,
				'h_volume_max': self.h_volume_max.value,
				'h_playlist_count': self.h_playlist_count.value
			}, f, indent=True)
