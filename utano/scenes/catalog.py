import tkinter

from nui.gui.v2 import Scene, Stage, Entry, SingleListbox

from core import Utano


class Catalog(Scene):  # TODO Search
	name = 'c'

	def __init__(self, stage: Stage, ut: Utano):
		super().__init__(stage)
		self.ut: Utano = ut

		self.v_search = tkinter.StringVar()
		self.v_search.trace_add("write", lambda *args: self.filter(self.e_search.get()))  # TODO Escape if empty
		self.e_search = Entry(self, style=self.style.alter_clone(font_size=10), textvariable=self.v_search)
		self.l_catalog = SingleListbox(self, parse_method=lambda s: s.get_full_name(self.ut.config.reverse_in_list), style=self.style.alter_clone(font_size=10)) \
			.inline_bind("i", lambda _: self.e_search.focus_set()) \
			.inline_bind("<BackSpace>", lambda _: self.e_search.focus_set()) \
			.inline_select_bind(self.selected)

		self.e_search.inline_bind("<Up>", lambda _: self.l_catalog.focus_set()) \
			.inline_bind("<Down>", lambda _: self.l_catalog.focus_set()) \
			.inline_bind("<Return>", lambda _: self.selected(self.l_catalog.get_())) \
			.inline_pack()

		self.l_catalog.inline_pack()

	def activate(self, whisper=None):
		super().activate()
		self.e_search.delete(0, 'end')
		self.filter(i=self.ut.actual_i)
		self.e_search.focus_set()

	def filter(self, reg='', i=0):
		values = []
		for s in self.ut.songs:
			f = s.get_full_name(self.ut.config.reverse_in_list)
			if tkinter.re.match(r'.*{}.*'.format(tkinter.re.escape(reg)), f, tkinter.re.IGNORECASE):
				values.append(s)  # TODO Somehow remove this temp list
		self.l_catalog.set_values(values)
		# self.l_catalog.config(width=int(width * 0.8))
		self.l_catalog.activate(i)
		self.l_catalog.selection_set(i)

	def selected(self, song):
		self.ut.play_this(song)
		self.stage.switch('')

	def typed(self, event) -> None:
		if event.keysym == 'Escape':
			self.stage.switch('')
