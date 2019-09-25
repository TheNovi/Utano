import tkinter
from random import sample

from scenes.scene import Scene
from utano.lyrics import Lrc, Drop


class _DropWrapper:  # TODO Void
	def __init__(self, main):
		self.main = main
		self.a = -1
		self.off = 0
		self.sn = ''
		self.sa = ''
		self.spaces_n, self.spaces_a = '', ''
		self.shuffle, self.move, self.void = True, True, False

	def set(self, duration, offset, options):
		if self.a > 0:
			self.stop()
		self.a: int = duration*2
		self.off = offset*3
		self.sn = self.main.l_name.cget('text')
		self.sa = self.main.l_artist.cget('text')
		self.spaces_n = tkinter.re.match(r"\s*", self.sn).group()
		self.spaces_a = tkinter.re.match(r"\s*", self.sa).group()
		self.shuffle, self.move, self.void = 's' not in options, 'm' not in options, 'v' in options

	def tick(self):
		self.a -= 1
		sn, sa = self.sn, self.sa
		if self.shuffle:
			sn = sn.strip()
			sa = sa.strip()
			sn = f'{self.spaces_n}{"".join(sample(sn, len(sn)))}{self.spaces_n}'
			sa = f'{self.spaces_a}{"".join(sample(sa, len(sa)))}{self.spaces_a}'

		if self.a % 2:
			self.main.l_name['text'] = sn[self.off:] + (' '*self.off)
			self.main.l_artist['text'] = sa[self.off:] + (' ' * self.off)
		else:
			self.main.l_name['text'] = (' ' * self.off) + sn[:self.off*-1]
			self.main.l_artist['text'] = (' ' * self.off) + sa[:self.off*-1]
		if self.a <= 0:
			self.stop()

	def stop(self):
		self.a = -1
		self.main.l_name['text'] = self.sn
		self.main.l_artist['text'] = self.sa


# noinspection PyAttributeOutsideInit
class Main(Scene):
	def _init_(self):
		super()._init_()
		self.l_name = tkinter.Label(self, text='', bg=self.theme["bg"], fg=self.theme['fg'], font=(self.theme['font'], 25))
		self.l_artist = tkinter.Label(self, text='', bg=self.theme['bg'], fg=self.theme['fg'], font=(self.theme['font'], 15))
		self.song_line = tkinter.Label(self, bg=self.theme['bg'], fg=self.theme['fg'], font=('helvetica', 5))

		self.f_lrc = tkinter.Frame(self)
		self.l_lrc = tkinter.Label(self.f_lrc, bg=self.theme['bg'], fg=self.theme['lrc'], font=('Comic Sans MS', 20, 'italic'))
		self.drop = _DropWrapper(self)

		self.l_lrc.pack(fill='both')
		self.l_name.pack(fill='both')
		self.l_artist.pack(fill='both')
		self.song_line.pack(fill='both')

		for b in [
			('<Button-1>', lambda e: self.ut.next_song()),
			('<Button-3>', lambda e: self.ut.next_song(-1)),
			('<MouseWheel>', lambda event: self.manager.s_volume.switch_to_me() or self.manager.s_volume.vol_change_e(event))
		]:
			self.l_name.bind(*b)
			self.l_artist.bind(*b)
			self.song_line.bind(*b)

	def tick(self):
		self.u_song_line()
		if self.drop.a > 0:
			self.drop.tick()

	def u_song_line(self):
		p = (1 - self.ut.player.get_progress())
		p = min(1, max(0, p))
		self.song_line['text'] = '-' * int(p * self.song_line.winfo_width()/2.3)

	def typed(self, event):
		super().typed(event)
		if event.keysym == 'Down':
			self.manager.s_catalog.switch_to_me()  # FIXME Sometimes e_search don't get focused
		elif event.keysym == 'Up':
			self.manager.s_volume.switch_to_me()

	def next_song_call(self):
		def add_spaces(h, offset=30):  # Adding some spaces around names
			h = "   " + h + "   "
			while len(h) < offset:
				h = " " + h + " "
			return h
		self.drop.a = -1
		s = self.ut.get_actual_song()
		if s.lrc.active:
			self.f_lrc.pack(fill='both')
			self.l_lrc['text'] = ''
		else:
			self.f_lrc.pack_forget()
		self.l_name['text'] = add_spaces(s.name, 50 if s.lrc.active else 30)
		self.l_artist['text'] = add_spaces(s.artist, 50 if s.lrc.active else 30)

	def lrc_call(self, lrc):
		if isinstance(lrc, Lrc):
			self.l_lrc['text'] = "   " + lrc.text + "   "
		elif isinstance(lrc, Drop):
			self.drop.set(lrc.duration, lrc.offset, lrc.options)
