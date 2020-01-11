import tkinter
from random import sample

from scenes.scene import Scene


# noinspection PyAttributeOutsideInit
class Main(Scene):
	def _init_(self):
		super()._init_()
		self.manager.mod = 1  # TODO Delete me
		self.sub_select = []

		self.l_name = tkinter.Label(self, text='', bg=self.theme["bg"], fg=self.theme['fg'], font=(self.theme['font'], 25))
		self.l_artist = tkinter.Label(self, text='', bg=self.theme['bg'], fg=self.theme['fg'], font=(self.theme['font'], 15))
		self.song_line = tkinter.Label(self, bg=self.theme['bg'], fg=self.theme['fg'], font=('helvetica', 5))

		self.v_search = tkinter.StringVar()
		self.v_search.trace_add("write", lambda *args: self.filter(self.e_search.get()))
		self.e_search = tkinter.Entry(self, textvariable=self.v_search, bg=self.theme['bg'], fg=self.theme['fg'], font=(self.theme['font'], 10))
		self.l_catalog = tkinter.Listbox(self, bg=self.theme['bg'], fg=self.theme['fg'], font=(self.theme['font'], 10), highlightthickness=0, selectmode='SINGLE', height=10)

		self.l_name.pack(fill='both')
		self.l_artist.pack(fill='both')
		self.song_line.pack(fill='both')
		self.e_search.pack(fill='both')
		self.l_catalog.pack(fill='both')

		self.l_catalog.bind("<<ListboxSelect>>", lambda _: self.selected())
		self.l_catalog.bind("<Return>", lambda _: self.activated())
		self.l_catalog.bind("i", lambda _: self.e_search.focus_set())
		self.l_catalog.bind("<BackSpace>", lambda _: self.e_search.focus_set())
		self.e_search.bind("<Up>", lambda _: self.l_catalog.focus_set())
		self.e_search.bind("<Down>", lambda _: self.l_catalog.focus_set())
		self.e_search.bind("<Return>", lambda _: self.l_catalog.focus_set())

		b = ('<MouseWheel>', lambda event: self.manager.s_volume.switch_to_me() or self.manager.s_volume.vol_change_e(event))
		self.l_name.bind(*b)
		self.l_artist.bind(*b)
		self.song_line.bind(*b)

	def activate_mod(self):
		self.manager.mod = 1
		# self.utano.apply_song_select()
		self.manager.root.title('Utano: Guess mode')
		self.utano.next_song(len(self.utano.all_songs), False)
		self._clear()
		self.switch_to_me()

	def activate(self):
		super().activate()
		self.e_search.focus_force()

	def tick(self):
		pass

	def typed(self, event):
		if event.keysym == 'Left':
			self.manager.mod_changer.switch_to_me()

	# def next_song_call(self):
	# 	def add_spaces(h, offset=30):  # Adding some spaces around names
	# 		h = "   " + h + "   "
	# 		while len(h) < offset:
	# 			h = " " + h + " "
	# 		return h
	#
	# 	s = self.utano.get_actual_song()
	# 	min_spaces = 50 if s.lrc.active else 30
	# 	self.l_name['text'] = add_spaces(s.name, min_spaces)
	# 	self.l_artist['text'] = add_spaces(s.artist, min_spaces)

	def filter(self, reg=''):
		self.l_catalog.delete(0, 'end')
		self.sub_select = []
		if len(reg) < 3:  # FIXME What if song has 2 letter name? Do i even care?
			return
		width = 40
		for s in sample(self.utano.songs, len(self.utano.songs)):
			f = s.get_full_name(self.utano.config['reverse_in_list'])
			if tkinter.re.match(r'.*{}.*'.format(tkinter.re.escape(reg)), f, tkinter.re.IGNORECASE):
				self.l_catalog.insert('end', f)
				self.sub_select.append(s)
				if len(f) > width:
					width = len(f)
		self.l_catalog.config(width=int(width * 0.8))
		# self.l_catalog.activate(i)
		self.l_catalog.select_clear(0, 'end')

	# self.l_catalog.select_set(i)

	def selected(self):  # Selected by mouse
		self.l_catalog.focus_set()
		if self.l_catalog.curselection() != ():
			s = self.l_catalog.curselection()
			self.answer(self.sub_select[s[0]])

	def activated(self):  # Selected by <Return>
		s = self.l_catalog.index('active')
		self.answer(self.sub_select[s])

	def answer(self, song):  # TODO Some notif
		if song == self.utano.get_actual_song():
			print("Yes")
			self.utano.next_song(stat=self.utano.stats.CheatSheet.songs_guessed_correctly)
		else:
			print('No')
			self.utano.next_song(stat=self.utano.stats.CheatSheet.songs_guessed_incorrectly)
		self._clear()

	def _clear(self):
		self.e_search.delete(0, 'end')
		self.filter()
		self.e_search.focus_set()
