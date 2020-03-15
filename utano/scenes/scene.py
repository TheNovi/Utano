from tkinter import Frame

from utano import Utano
from utano import scenes


class Scene(Frame):
	def __init__(self, master, manager: 'scenes.ScenesManager', utano: Utano, theme, **kw):
		super().__init__(master, bg=theme['bg'], **kw)
		self.manager: 'scenes.ScenesManager' = manager
		self.utano: Utano = utano
		self.theme = theme
		self._init_()

	def _init_(self):
		# Overwrite me
		pass

	def activate(self):
		self.pack(fill='both')

	def activate_mod(self):  # Called when mod is switched
		pass

	def tick(self):
		# Overwrite me
		pass

	def deactivate(self):
		self.pack_forget()

	def typed(self, event):
		# Overwrite me
		pass

	def switch_to_me(self):
		self.manager.switch(self)
