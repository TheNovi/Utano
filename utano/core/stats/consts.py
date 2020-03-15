class _Event:
	def __init__(self, name, xp):
		self.name = name
		self.xp = xp

	def __eq__(self, other):
		return self.name == other


stats_created = _Event('stats created', 0)
program_started = _Event('program started', 0)
song_played = _Event('song played', 3)
song_skipped = _Event('song skipped', 1)
paused = _Event('paused', 0)
song_replayed = _Event('song replayed', 1)
song_selected = _Event('song selected', 2)
playlist_completed = _Event('playlist completed', 10)
total_time = _Event('total time', 0)
songs_guessed_correctly = _Event('songs guessed correctly', 5)
songs_guessed_incorrectly = _Event('songs guessed incorrectly', 1)
h_volume_max = _Event('h_volume max', 0)
h_playlist_count = _Event('h_playlist count', 0)
