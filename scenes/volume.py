import tkinter

from scenes.scene import Scene


class Volume(Scene):
	def _init_(self):
		self.v_volume = tkinter.IntVar()
		self.l_volume = tkinter.Label(self, textvariable=self.v_volume, bg=self.theme['bg'], fg=self.theme['fg'], font=(self.theme['font'], 25), padx=200, pady=28)

		self.l_volume.bind("<MouseWheel>", self.vol_change_e)

		self.l_volume.pack(fill='both')

	def activate(self):
		super().activate()
		self.v_volume.set(self.ut.player.p.audio_get_volume())

	def tick(self):
		pass

	def typed(self, event):
		if event.char == 'v':
			self.manager.escape()

	def vol_change_e(self, event):
		a = int(self.ut.player.p.audio_get_volume()+event.delta/120)
		self.ut.player.p.audio_set_volume(min(a, 100))
		self.master.after(1)
		self.v_volume.set(self.ut.player.p.audio_get_volume())
