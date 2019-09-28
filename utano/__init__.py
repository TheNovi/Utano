from typing import List, Callable
from random import shuffle
from glob import glob
from datetime import datetime

from . import song, player, stats


class Utano:
	def __init__(self, config):
		self.next_song_call = print
		self.lrc_call = print
		self.config = config
		self.songs: List[song.Song] = []
		self.player = player.Player(self.config, lambda: self.next_song(stat=stats.Stats.CheatSheet.song_played))
		self.stats = stats.Stats(config['stats_path'])

		self.actual_i = -1
		self.status = True  # Playing/Paused
		self._time_buffer = 0
		self._time_now = None

		self._load_songs_()
		self.stats.set(self.stats.CheatSheet.h_playlist_count, len(self.songs))
		shuffle(self.songs)

	def _load_songs_(self):
		self.songs = [song.Song(path) for path in glob(self.config["path"] + '*.*')]

	def set_callbacks(self, next_song_call: Callable, lrc_call: Callable):
		self.next_song_call = next_song_call
		self.lrc_call = lrc_call

	def get_actual_song(self):
		return self.songs[self.actual_i]

	def next_song(self, i=1, stat=stats.Stats.CheatSheet.song_skipped):
		self.actual_i += i
		if self.actual_i >= len(self.songs):
			self.actual_i = 0
			shuffle(self.songs)
			self.stats.add(self.stats.CheatSheet.playlist_completed)
		elif self.actual_i < 0:
			self.actual_i = len(self.songs) - 1

		if stat:
			self.stats.add(self.stats.CheatSheet.total_time, int(self.get_time()/1000))
		self._time_buffer = 0
		self._time_now = datetime.now()
		self.player.play(self.get_actual_song(), self.status)
		if i <= 0 and stat == stats.Stats.CheatSheet.song_skipped:
			self.stats.add(self.stats.CheatSheet.song_replayed)
		else:
			self.stats.add(stat)
		self.next_song_call()

	def play_this(self, s: song):
		self.actual_i = self.songs.index(s)
		self.next_song(0, self.stats.CheatSheet.song_selected)

	def tick(self):
		self.player.tick()
		if self.status and self.get_actual_song().lrc.active:
			time = self.get_time()
			lrc = self.get_actual_song().lrc.tick(time)
			if lrc:
				self.lrc_call(lrc)

	def get_time(self):
		return self._time_buffer if not self.status else int(self._time_buffer + ((datetime.now() - self._time_now).total_seconds() * 1000))

	def pause(self):
		if self.status:
			self._time_buffer = self.get_time()
			self.stats.add(self.stats.CheatSheet.paused)
			self.player.pause()
		else:
			self._time_now = datetime.now()
			self.player.un_pause()
		self.status = not self.status

	def end(self):
		self.stats.add(self.stats.CheatSheet.total_time, int(self.get_time()/1000))
		self.stats.save()
