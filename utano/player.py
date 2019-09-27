import vlc

from .song import Song


class Player:
	def __init__(self, conf, song_ended_call):
		# self._p: vlc.MediaPlayer = vlc.MediaPlayer()
		self._inst_ = vlc.Instance("--no-xlib")  # TODO Release after
		self._p: vlc.MediaPlayer = self._inst_.media_player_new()
		self.sec = song_ended_call
		self.apply_conf(conf)

	def tick(self):
		if self._p.get_state().value > 5:
			self.sec()

	def apply_conf(self, conf):
		self._p.audio_set_volume(conf["volume"])

	def play(self, m: Song, status):
		self._p.set_mrl(m.path)
		m.reset()
		if status:
			self._p.play()
		# self._p.set_position(0.95)

	def pause(self):
		self._p.pause()

	def un_pause(self):
		self._p.play()

	def get_progress(self):
		return self._p.get_position()

	def get_time(self):
		return self._p.get_time()

	def get_length(self):
		return self._p.get_length()

	def set_volume(self, volume: int):
		self._p.audio_set_volume(min(volume, 100))

	def get_volume(self):
		return self._p.audio_get_volume()
