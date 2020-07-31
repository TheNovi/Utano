from datetime import datetime
from glob import glob
from random import shuffle
from typing import List, Callable

from . import song, player, stats


class Utano:
	def __init__(self, config):
		self.next_song_call = print
		self.lrc_call = print
		self.config = config
		self.all_songs: List[song.Song] = []
		self.songs: List[song.Song] = []
		self.stats = stats.Stats(config)
		self.player = player.Player(self.config, lambda: self.next_song(stat=self.stats.song_played))

		self.actual_i = -1
		self.status = not config['start_paused']  # Playing/Paused
		self._time_buffer = 0
		self._time_now = None

		self._load_all_songs_()
		if len(self.songs) > 100:
			self.stats.h_playlist_count.set(1)
		shuffle(self.songs)

	def _load_all_songs_(self):
		self.all_songs = [song.Song(path, self.config) for path in glob(f"{self.config['path']}/**/*.*")]  # TODO Ignore non audio files
		self.all_songs += [song.Song(path, self.config) for path in glob(f"{self.config['path']}/*.*")]
		self.songs = self.all_songs

	def set_callbacks(self, next_song_call: Callable, lrc_call: Callable, achieve_call: Callable):
		self.next_song_call = next_song_call
		# self.stats.set_callback(achieve_call) # TODO
		self.lrc_call = lrc_call

	def apply_song_select(self, songs: List[song.Song] = None):
		if songs:
			self.songs = songs
		else:
			self.songs = self.all_songs
		self.actual_i = 0
		self.next_song(0)

	def get_actual_song(self):
		return self.songs[self.actual_i]

	def next_song(self, i=1, stat=None, playlist_completed=True, init=False):
		if stat is None:
			stat = self.stats.song_skipped

		if self.config['auto_play'] and self.actual_i >= 0:
			self.status = True
		if i == -1:
			stat = self.stats.song_replayed
			if self.config['replay_when_progress'] > 0 and self.get_time() > self.config['replay_when_progress'] * 1000:
				i = 0
		self.actual_i += i
		if self.actual_i >= len(self.songs):
			self.actual_i = 0
			shuffle(self.songs)
			if playlist_completed:  # TODO Check me: not sure what playlist_completed is
				self.stats.playlist_completed.add()
		elif self.actual_i < 0:
			self.actual_i = len(self.songs) - 1

		self.stats.total_time.add(int(self.get_time() / 1000))
		self._time_buffer = 0
		self._time_now = datetime.now()
		self.player.play(self.get_actual_song(), self.status)
		if not init:
			stat.add()
		self.next_song_call()

	def play_this(self, s: song):
		self.actual_i = self.songs.index(s)
		self.next_song(0, self.stats.song_selected)

	def tick(self):
		self.player.tick()
		if self.status and self.get_actual_song().lrc.active:
			time = self.get_time()
			lrc = self.get_actual_song().lrc.tick(time)
			if lrc:
				self.lrc_call(lrc)

	def get_time(self):
		if not self._time_now:
			return 0
		return self._time_buffer if not self.status else int(self._time_buffer + ((datetime.now() - self._time_now).total_seconds() * 1000))

	def pause(self):
		if self.status:
			self._time_buffer = self.get_time()
			self.stats.paused.add()
			self.player.pause()
		else:
			self._time_now = datetime.now()
			self.player.un_pause()
		self.status = not self.status

	def end(self):
		self.stats.total_time.add(int(self.get_time() / 1000))
		self.stats.save()
		self.player.end()
