import json


class Stats:
	_stats = [
		'program started',
		'song played',
		'song skipped',
		'paused',
		'song replayed',
		'song selected',
		'playlist completed',
		'total time',

		'h_volume max',
		'h_playlist count'
	]

	class CheatSheet:
		program_started = 'program started'
		song_played = 'song played'
		song_skipped = 'song skipped'
		paused = 'paused'
		song_replayed = 'song replayed'
		song_selected = 'song selected'
		playlist_completed = 'playlist completed'
		total_time = 'total time'

		h_volume_max = 'h_volume max'
		h_playlist_count = 'h_playlist count'

	def __init__(self, path):
		self.path = path
		self.stats = self._load()

	def set(self, key, count):
		if not key:
			return
		self.stats[key] = count
		# [x.check() for x in Stats.achievements if not x.got_it or x.max_count]

	def add(self, key, count=1):
		if not key:
			return
		self.stats[key] += count
		# [x.check() for x in Stats.achievements if not x.got_it or x.max_count]

	def _load(self):
		c = {}
		try:
			with open(self.path, 'r') as f:
				c = json.load(f)
		except Exception as e:
			print(e)
		for k in Stats._stats:
			if k not in c:
				c[k] = 0
		return c

	def save(self):
		with open(self.path, 'w') as f:
			json.dump(self.stats, f, indent=1)
