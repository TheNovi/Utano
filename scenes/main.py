import tkinter

from scenes.scene import Scene


# noinspection PyAttributeOutsideInit
class Main(Scene):
	def _init_(self):
		super()._init_()
		# self.v_name = tkinter.StringVar()
		# self.v_artist = tkinter.StringVar()
		self.l_artist = tkinter.Label(self, text='', bg=self.theme['bg'], fg=self.theme['fg'], font=(self.theme['font'], 15))
		self.l_name = tkinter.Label(self, text='', bg=self.theme["bg"], fg=self.theme['fg'], font=(self.theme['font'], 25))
		self.song_line = tkinter.Label(self, bg=self.theme['bg'], fg=self.theme['fg'], font=('helvetica', 5))

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

		# self.l_name.bind("<Button-1>", lambda e: self.ut.next_song())
		# self.l_name.bind("<Button-3>", lambda e: self.ut.next_song(-1))
		# self.l_artist.bind("<Button-1>", lambda e: self.ut.next_song())
		# self.l_artist.bind("<Button-3>", lambda e: self.ut.next_song(-1))
		# self.bind("<MouseWheel>", lambda event: self.manager.s_volume.switch_to_me() or self.manager.s_volume.vol_change_e(event))

	def tick(self):
		self.u_song_line()

	def u_song_line(self):
		p = (1 - self.ut.player.get_progress())
		p = min(1, max(0, p))
		self.song_line['text'] = '-' * int(p * self.song_line.winfo_width()/2.3)

	def typed(self, event):
		super().typed(event)
		if event.keysym == 'Down':
			self.manager.s_catalog.switch_to_me()

	def next_song_call(self):
		def add_spaces(h):  # Adding some spaces around names
			h = "   " + h + "   "
			while len(h) < 30:
				h = " " + h + " "
			return h
		s = self.ut.get_actual_song()
		self.l_name['text'] = add_spaces(s.name)
		self.l_artist['text'] = add_spaces(s.artist)
