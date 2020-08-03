import json
from os.path import exists, join, dirname


class Conf:
	def __init__(self, path_prefix):
		self.__path_prefix = path_prefix
		self.__conf_path_prefix = path_prefix
		self.raw_conf_path = 'home/conf.json'
		self.raw_music_path = 'music'
		self.raw_theme_path = 'theme.json'
		self.raw_stats_path = 'stats.json'
		self.raw_lrc_path = 'lrc'
		self.volume = 50
		self.replay_when_progress = 0
		self.start_paused = False
		self.auto_play = False
		self.disable_stop_button = True
		self.switch_controls = False
		self.reverse_title = True
		self.reverse_in_list = False

	@property
	def conf_path(self):
		return join(self.__path_prefix, self.raw_conf_path)

	@property
	def music_path(self):
		return join(self.__conf_path_prefix, self.raw_music_path)

	@property
	def theme_path(self):
		return join(self.__conf_path_prefix, self.raw_theme_path)

	@property
	def stats_path(self):
		return join(self.__conf_path_prefix, self.raw_stats_path)

	@property
	def lrc_path(self):
		return join(self.__conf_path_prefix, self.raw_lrc_path)

	def load(self, path: str) -> 'Conf':
		self.raw_conf_path = path
		self.__conf_path_prefix = dirname(self.conf_path)
		print(self.conf_path)
		if exists(self.conf_path):
			with open(self.conf_path) as f:
				d = json.load(f)
			self.raw_music_path = d.get('music_path', d.get('path', self.music_path))
			self.raw_theme_path = d.get('theme_path', self.theme_path)
			self.raw_stats_path = d.get('stats_path', self.stats_path)
			self.raw_lrc_path = d.get('lrc_path', self.lrc_path)
			self.volume = d.get('volume', self.volume)
			self.start_paused = d.get('start_paused', self.start_paused)
			self.auto_play = d.get('auto_play', self.auto_play)
			self.replay_when_progress = d.get('replay_when_progress', self.replay_when_progress)
			self.disable_stop_button = d.get('disable_stop_button', self.disable_stop_button)
			self.switch_controls = d.get('switch_controls', self.switch_controls)
			self.reverse_title = d.get('reverse_title', self.reverse_title)
			self.reverse_in_list = d.get('reverse_in_list', self.reverse_in_list)
		else:
			print('Conf file not found')
		print(self.music_path)
		print(self.theme_path)
		print(self.stats_path)
		print(self.lrc_path)
		return self

	def save(self):
		with open(self.conf_path, 'w') as f:
			json.dump({
				'music_path': self.raw_music_path,
				'theme_path': self.raw_theme_path,
				'stats_path': self.raw_stats_path,
				'lrc_path': self.raw_lrc_path,
				'volume': self.volume,
				'start_paused': self.start_paused,
				'auto_play': self.auto_play,
				'replay_when_progress': self.replay_when_progress,
				'disable_stop_button': self.disable_stop_button,
				'switch_controls': self.switch_controls,
				'reverse_title': self.reverse_title,
				'reverse_in_list': self.reverse_in_list
			}, f, indent=True)
