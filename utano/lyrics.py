from os import path

import utano


class Drop:
	def __init__(self, text):
		self.time = int(text[0].replace("[", "").replace(" ", "").strip(" "))
		text = text[1].strip().split(' ')
		text.append('')
		self.duration = text[1]
		self.offset = text[2]
		self.options = text[3]
		self.text = 'drop'


class Lrc:
	def __init__(self, text):
		self.time = int(text[0].replace("[", "").replace(" ", "").strip())
		self.text = text[1].strip().replace("\\n", "\n")


class Lyrics:
	def __init__(self, song: 'utano.song.Song'):
		self.que = []
		self._i = 0
		self.active = True
		self.lrc = True
		self.drops = True
		self.void = False
		if not path.exists(f"nudes/lrc/{song.get_full_name()}.lc"):
			self.active = False
			return
		with open(f"nudes/lrc/{song.get_full_name()}.lc", encoding='utf-8') as lc:
			text = lc.readlines()
		for t in text:
			t = t.replace('\n', "").strip(" ")
			if len(t) == 0 or t[0] in ['#', '/'] or t[0] not in ['[', '!']:
				continue
			if t[0] == '!':
				if t == '!all':
					self.active = False
					break
				elif t == '!lrc':
					self.lrc = False
				elif t == '!drop':
					self.drops = False
				elif t == '!void':
					self.void = True
				continue
			t = t.split("]")
			if t[1].strip().startswith('!drop'):
				if self.drops:
					self.que.append(Drop(t))
			elif self.lrc:
				self.que.append(Lrc(t))

	def tick(self, time: int):
		if self._i >= len(self.que):
			return
		if time > self.que[self._i].time:
			self._i += 1
			return self.que[self._i-1]

	def reset(self):
		self._i = 0
