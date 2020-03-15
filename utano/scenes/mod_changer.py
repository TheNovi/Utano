import tkinter

from .scene import Scene


# noinspection PyAttributeOutsideInit
class ModChanger(Scene):
	def _init_(self):
		super()._init_()
		self.tmp_mods = [
			{'n': 'Main', 'm': self.manager.s_main.activate_mod},
			{'n': 'Guess game', 'm': self.manager.gue_main.activate_mod}
		]
		self.sub_select = []

		self.v_search = tkinter.StringVar()
		self.v_search.trace_add("write", lambda *args: self.filter(self.e_search.get()))
		self.e_search = tkinter.Entry(self, textvariable=self.v_search, bg=self.theme['bg'], fg=self.theme['fg'], font=(self.theme['font'], 10))
		self.l_catalog = tkinter.Listbox(self, bg=self.theme['bg'], fg=self.theme['fg'], font=(self.theme['font'], 10), highlightthickness=0, selectmode='SINGLE', height=10)

		self.l_catalog.bind("<<ListboxSelect>>", lambda _: self.selected())
		self.l_catalog.bind("<Return>", lambda _: self.activated())
		self.l_catalog.bind("i", lambda _: self.e_search.focus_set())
		self.l_catalog.bind("<BackSpace>", lambda _: self.e_search.focus_set())
		self.e_search.bind("<Up>", lambda _: self.l_catalog.focus_set())
		self.e_search.bind("<Down>", lambda _: self.l_catalog.focus_set())
		self.e_search.bind("<Return>", lambda _: self.l_catalog.focus_set())

		self.e_search.pack(fill='both')
		self.l_catalog.pack(fill='both')

	def typed(self, event):
		if event.keysym == 'Right':
			self.manager.escape()

	def activate(self):
		super().activate()
		self.e_search.delete(0, 'end')
		self.filter(i=self.manager.mod)
		self.e_search.focus_set()

	def filter(self, reg='', i=0):
		self.l_catalog.delete(0, 'end')
		self.sub_select = []
		width = 40
		for s in self.tmp_mods:
			f = s['n']
			if tkinter.re.match(r'.*{}.*'.format(tkinter.re.escape(reg)), f, tkinter.re.IGNORECASE):
				self.l_catalog.insert('end', f)
				self.sub_select.append(s)
				if len(f) > width:
					width = len(f)
		self.l_catalog.config(width=int(width * 0.8))
		self.l_catalog.activate(i)
		self.l_catalog.select_clear(0, 'end')
		self.l_catalog.select_set(i)

	def selected(self):  # Selected by mouse
		self.l_catalog.focus_set()
		if self.l_catalog.curselection() != ():
			s = self.l_catalog.curselection()
			s = self.sub_select[s[0]]
			s['m']()

	def activated(self):  # Selected by <Return>
		s = self.l_catalog.index('active')
		s = self.sub_select[s]
		s['m']()
