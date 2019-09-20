from tkinter import Frame

from utano import Utano
import scenes


class Scene(Frame):
	def __init__(self, master, manager: 'scenes.ScenesManager', utano: Utano, theme, **kw):
		super().__init__(master, bg=theme['bg'], **kw)
		self.manager: 'scenes.ScenesManager' = manager
		self.ut: Utano = utano
		self.theme = theme
		self._init_()

	def _init_(self):
		pass

	def activate(self):
		self.pack(fill='both')

	def tick(self):
		pass

	def deactivate(self):
		self.pack_forget()

	def typed(self, event):
		pass
