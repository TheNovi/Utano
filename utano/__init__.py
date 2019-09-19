from typing import List, Callable
from random import shuffle
from glob import glob

from . import song, player


class Utano:
	def __init__(self, config):
		self.next_song_call = print
		self.config = config
		self.songs: List[song.Song] = []
		self.player = player.Player(self.config, self.next_song)

		self._actual_i_ = -1
		self.status = True  # Playing/Paused

		self._load_songs_()
		shuffle(self.songs)

	def _load_songs_(self):
		self.songs = [song.Song(path) for path in glob(self.config["path"] + '*.*')]

	def set_callbacks(self, next_song_call: Callable):
		self.next_song_call = next_song_call

	def get_actual_song(self):
		return self.songs[self._actual_i_]

	def next_song(self, i=1):
		self._actual_i_ += i
		if self._actual_i_ >= len(self.songs):
			self._actual_i_ = 0
			shuffle(self.songs)
		elif self._actual_i_ < 0:
			self._actual_i_ = len(self.songs) - 1

		self.player.play(self.get_actual_song(), self.status)
		self.next_song_call()

	def tick(self):
		self.player.tick()
		pass

	def pause(self):
		if self.status:
			self.player.pause()
		else:
			self.player.un_pause()
		self.status = not self.status
