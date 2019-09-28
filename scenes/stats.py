import tkinter
from datetime import timedelta

from scenes.scene import Scene


# noinspection PyAttributeOutsideInit
class Stats(Scene):
	def _init_(self):
		super()._init_()
		self.l_title = tkinter.Label(self, text="Your statistics", bg=self.theme["bg"], fg=self.theme['fg'], font=(self.theme['font'], 10))
		self.l_line = tkinter.Label(self, text=12 * '----------', bg=self.theme["bg"], fg=self.theme['fg'], font=('helvetica', 5))
		self.f_stats = tkinter.Frame(self)

		self.l_title.pack(fill='both')
		self.l_line.pack(fill='both')

	def activate(self):
		self.f_stats.destroy()
		self.f_stats = tkinter.Frame(self)
		for key, value in self.ut.stats.stats.items():
			if key.startswith('h_'):
				continue
			f_tmp = tkinter.Frame(self.f_stats)
			if key == self.ut.stats.CheatSheet.total_time:
				value = str(timedelta(seconds=value+int(self.ut.get_time()/1000))).split('.')[0]
			bg = self.theme['bg'] if len(self.f_stats.winfo_children()) % 2 else '#333333'
			tkinter.Label(f_tmp, text=key + ': ', bg=bg, fg=self.theme['fg'], anchor='w', font=(self.theme['font'], 10)).pack(fill='x', side='left')
			tkinter.Label(f_tmp, text=value, bg=bg, fg=self.theme['fg'], anchor='e', font=(self.theme['font'], 10)).pack(fill='x', side='right', expand=True)
			f_tmp.pack(fill='both')
		self.f_stats.pack(fill='both')
		super().activate()

	def typed(self, event):
		super().typed(event)
		if event.keysym == 'Down':
			self.manager.s_catalog.switch_to_me()  # FIXME Sometimes e_search don't get focused
		elif event.keysym == 'Up':
			self.manager.s_volume.switch_to_me()
		elif event.keysym == 'Right':
			self.manager.s_achieve.switch_to_me()
		elif event.keysym == 'Left':
			self.manager.escape()

