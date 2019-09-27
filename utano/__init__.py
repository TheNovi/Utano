from typing import List, Callable
from random import shuffle
from glob import glob

from . import song, player


class Utano:
	def __init__(self, config):
		self.next_song_call = print
		self.lrc_call = print
		self.config = config
		self.songs: List[song.Song] = []
		self.player = player.Player(self.config, self.next_song)

		self.actual_i = -1
		self.status = True  # Playing/Paused

		self._load_songs_()
		shuffle(self.songs)

	def _load_songs_(self):
		self.songs = [song.Song(path) for path in glob(self.config["path"] + '*.*')]

	def set_callbacks(self, next_song_call: Callable, lrc_call: Callable):
		self.next_song_call = next_song_call
		self.lrc_call = lrc_call

	def get_actual_song(self):
		return self.songs[self.actual_i]

	def next_song(self, i=1):
		self.actual_i += i
		if self.actual_i >= len(self.songs):
			self.actual_i = 0
			shuffle(self.songs)
		elif self.actual_i < 0:
			self.actual_i = len(self.songs) - 1

		self.player.play(self.get_actual_song(), self.status)
		self.next_song_call()

	def play_this(self, s: song):
		self.actual_i = self.songs.index(s)
		self.next_song(0)

	def tick(self):
		self.player.tick()
		if self.status and self.get_actual_song().lrc.active:
			time = self.player.get_time()  # FIXME Lags
			lrc = self.get_actual_song().lrc.tick(time)
			if lrc:
				self.lrc_call(lrc)
				# print(lrc.text)
			# print(self.get_actual_song().lrc.get_p_bar(self.player.get_length(), time))

	def pause(self):
		if self.status:
			self.player.pause()
		else:
			self.player.un_pause()
		self.status = not self.status
