import tkinter
from datetime import datetime

from scenes.scene import Scene


# noinspection PyAttributeOutsideInit
class Volume(Scene):
	COUNTDOWN = 3

	def _init_(self):
		super()._init_()
		self.timer = datetime.now()
		self.v_volume = tkinter.IntVar()
		self.l_volume = tkinter.Label(self, textvariable=self.v_volume, bg=self.theme['bg'], fg=self.theme['fg'], font=(self.theme['font'], 25), padx=200, pady=28)

		self.l_volume.bind('<MouseWheel>', self.vol_change_e)

		self.l_volume.pack(fill='both')

	def activate(self):
		super().activate()
		self.timer = datetime.now()
		self.v_volume.set(self.ut.player.get_volume())
		self.l_volume.config(fg=self.theme['fg'])

	def tick(self):
		b = self.winfo_rgb(self.theme['bg'])
		f = self.winfo_rgb(self.theme['fg'])
		p = 1 - round((datetime.now() - self.timer).total_seconds() / Volume.COUNTDOWN, 3)
		self.l_volume.config(fg='#' + ''.join([format(int((b[i] + (f[i]-b[i]) * min(p + 0.1, 1)) / 256), 'x').zfill(2) for i in range(3)]))
		if p <= 0:
			self.manager.escape()

	def typed(self, event):
		super().typed(event)
		if event.keysym == 'Down':
			self.manager.s_catalog.switch_to_me()

	def vol_change_e(self, event):
		self.timer = datetime.now()
		a = int(self.ut.player.get_volume() + event.delta / 120)
		self.ut.player.set_volume(a)
		if a > 100:
			self.ut.stats.set(self.ut.stats.CheatSheet.h_volume_max, 1)
		self.master.after(2)
		self.v_volume.set(self.ut.player.get_volume())
