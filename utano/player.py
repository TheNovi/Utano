import vlc

from .song import Song


class Player:
	def __init__(self, conf, song_ended_call):
		# self.p: vlc.MediaPlayer = vlc.MediaPlayer()
		self._inst_ = vlc.Instance("--no-xlib")  # TODO Release after
		self.p: vlc.MediaPlayer = self._inst_.media_player_new()
		self.sec = song_ended_call
		self.apply_conf(conf)

	def tick(self):
		if self.p.get_state().value > 5:
			self.sec()

	def apply_conf(self, conf):
		self.p.audio_set_volume(conf["volume"])

	def play(self, m: Song, status):
		self.p.set_mrl(m.path)
		if status:
			self.p.play()
		# self.p.set_position(0.95)

	def pause(self):
		self.p.pause()

	def un_pause(self):
		self.p.play()
