# from mutagen.mp3 import MP3


class Song:
	def __init__(self, path: str):
		self.path: str = path
		# self.mut = MP3(path)
		self.name, self.artist = self.get_name()

	# Getting song name/artist from file path
	def get_name(self):
		def cut_off_spaces_in_name(h):  # Adding some spaces around names
			h = "   " + str(h).strip(" ") + "   "
			while len(h) < 30:
				h = " " + h + " "
			return h
		t = self.path.replace("\\", "/").split("/")[-1]
		t = ''.join(t.split(".")[:-1])
		if ' - ' in t:
			return cut_off_spaces_in_name(t.split(' - ')[1]), cut_off_spaces_in_name(t.split(' - ')[0])
		return cut_off_spaces_in_name(t), ''
