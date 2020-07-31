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

	def __init__(self, config: dict):
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

		self.achievements: List[Achievement] = [
			Achievement(self, "Some achieve", "Desc", [self.song_played], 10)
		]

		self.config: dict = config
		self.load()

		if self.stats_created.value == 0:
			self.stats_created.set(datetime.now().strftime("%Y-%m-%d %H:%M"))

	def load(self):
		if path_exists(self.config['stats_path']):
			try:
				with open(self.config['stats_path']) as f:
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

	def save(self):
		with open(self.config['stats_path'], 'w') as f:
			json.dump(self.json(), f, indent=True)

	def json(self):
		return {
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
		}
