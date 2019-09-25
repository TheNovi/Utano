from utano.lyrics import Lyrics


class Song:
	def __init__(self, path: str):
		self.path: str = path
		self.name, self.artist = self._get_name()
		self.lrc = Lyrics(self)

	# Getting song name/artist from file path
	def _get_name(self):
		t = self.path.replace("\\", "/").split("/")[-1]
		t = ''.join(t.split(".")[:-1])
		if ' - ' in t:
			return t.split(' - ')[1], t.split(' - ')[0]
		return t, ''

	def reset(self):
		self.lrc.reset()

	def get_full_name(self):
		return self.artist + ' - ' + self.name
