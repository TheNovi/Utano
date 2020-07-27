import tkinter

from nui.gui.v1 import Scene, Stage, Entry, Listbox

from core import Utano


class Catalog(Scene):
	def __init__(self, stage: Stage, ut: Utano):
		super().__init__(stage)
		self.ut: Utano = ut
		self.sub_select = []

		self.v_search = tkinter.StringVar()
		self.v_search.trace_add("write", lambda *args: self.filter(self.e_search.get()))  # TODO Escape if empty
		self.e_search = Entry(self, style=self.style.child(font=(self.style.font, 10)), textvariable=self.v_search)
		self.l_catalog = Listbox(self, style=self.style.child(font=(self.style.font, 10)), highlightthickness=0, height=10) \
			.inline_bind("<<ListboxSelect>>", lambda _: self.selected()) \
			.inline_bind("<Return>", lambda _: self.activated()) \
			.inline_bind("i", lambda _: self.e_search.focus_set()) \
			.inline_bind("<BackSpace>", lambda _: self.e_search.focus_set())

		self.e_search.inline_bind("<Up>", lambda _: self.l_catalog.focus_set()) \
			.inline_bind("<Down>", lambda _: self.l_catalog.focus_set()) \
			.inline_bind("<Return>", lambda _: self.selected()) \
			.inline_pack()

		self.l_catalog.inline_pack()

	def activate(self):
		super().activate()
		self.e_search.delete(0, 'end')
		self.filter(i=self.ut.actual_i)
		self.e_search.focus_set()

	def filter(self, reg='', i=0):
		self.l_catalog.delete(0, 'end')
		self.sub_select = []
		width = 40
		for s in self.ut.songs:
			f = s.get_full_name(self.ut.config['reverse_in_list'])
			if tkinter.re.match(r'.*{}.*'.format(tkinter.re.escape(reg)), f, tkinter.re.IGNORECASE):
				self.l_catalog.insert('end', f)
				self.sub_select.append(s)
				if len(f) > width:
					width = len(f)
		self.l_catalog.config(width=int(width * 0.8))
		self.l_catalog.activate(i)
		self.l_catalog.select_clear(0, 'end')
		self.l_catalog.select_set(i)

	# TODO Use nui.Listbox methods
	def selected(self):  # Selected by mouse
		self.l_catalog.focus_set()
		if self.l_catalog.curselection() != ():
			s = self.l_catalog.curselection()
			s = self.sub_select[s[0]]
			self.ut.play_this(s)
			self.stage.switch('')

	def activated(self):  # Selected by <Return>
		s = self.l_catalog.index('active')
		s = self.sub_select[s]
		self.ut.play_this(s)
		self.stage.switch('')
