# from mutagen.mp3 import MP3


class Song:
	def __init__(self, path: str):
		self.path: str = path
		# self.mut = MP3(path)
		self.name, self.artist = self.get_name()

	# Getting song name/artist from file path
	def get_name(self):
		t = self.path.replace("\\", "/").split("/")[-1]
		t = ''.join(t.split(".")[:-1])
		if ' - ' in t:
			return t.split(' - ')[1], t.split(' - ')[0]
		return t, ''
