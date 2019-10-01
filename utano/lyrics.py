from os import path
from typing import Tuple

import utano


class Drop:
	def __init__(self, text):
		self.time = int(text[0].replace("[", "").replace(" ", "").strip(" "))
		text = text[1].strip().split(' ')
		text.append('')
		self.duration = int(text[1])
		self.offset = int(text[2])
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
		self._start = 0
		self.actual_text = ''
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
				if len(self.que) > 1 and self.que[-1].time < self.que[-2].time:
					self.que[-1].time = self.que[-2].time

	def tick(self, time: int):
		if self._i >= len(self.que):
			return
		lrc = self.que[self._i]
		if time > lrc.time:
			self._i += 1
			if not (isinstance(lrc, Drop)):
				self._start = lrc.time
				self.actual_text = lrc.text
			return self.que[self._i-1]

	def get_p_bar(self, ut) -> Tuple[float, bool]:
		def get_next_time():
			for lrc in self.que[self._i:]:
				if not (isinstance(lrc, Drop)):
					return lrc.time
			return ut.player.get_length()
		time = ut.get_time()
		end = get_next_time()
		out = (time-self._start)/max(1, end-self._start)
		return (out, True) if self.actual_text else (1-out, False)

	def reset(self):
		self._i = 0
