import tkinter

from scenes.scene import Scene
from utano.lyrics import Lrc, Drop


# noinspection PyAttributeOutsideInit
class Main(Scene):
	def _init_(self):
		super()._init_()
		self.l_artist = tkinter.Label(self, text='', bg=self.theme['bg'], fg=self.theme['fg'], font=(self.theme['font'], 15))
		self.l_name = tkinter.Label(self, text='', bg=self.theme["bg"], fg=self.theme['fg'], font=(self.theme['font'], 25))
		self.song_line = tkinter.Label(self, bg=self.theme['bg'], fg=self.theme['fg'], font=('helvetica', 5))

		self.f_lrc = tkinter.Frame(self)
		self.l_lrc = tkinter.Label(self.f_lrc, bg=self.theme['bg'], fg=self.theme['lrc'], font=('Comic Sans MS', 20, 'italic'))

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
		def add_spaces(h):  # Adding some spaces around names
			h = "   " + h + "   "
			while len(h) < 30:
				h = " " + h + " "
			return h
		s = self.ut.get_actual_song()
		if s.lrc.active:
			self.f_lrc.pack(fill='both')
			self.l_lrc['text'] = ''
		else:
			self.f_lrc.pack_forget()
		self.l_name['text'] = add_spaces(s.name)
		self.l_artist['text'] = add_spaces(s.artist)

	def lrc_call(self, lrc):
		if isinstance(lrc, Lrc):
			self.l_lrc['text'] = "   " + lrc.text + "   "
		elif isinstance(lrc, Drop):
			print('Drop')
