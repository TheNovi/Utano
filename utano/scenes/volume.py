from datetime import datetime

from nui.gui.v1 import Scene, Stage, Label

from core import Utano


class Volume(Scene):
	COUNTDOWN = 3

	def __init__(self, stage: Stage, ut: Utano, *args, **kwargs):
		super().__init__(stage, *args, **kwargs)
		self.timer = datetime.now()
		self.ut: Utano = ut

		# noinspection PyTypeChecker
		self.l_volume = Label(self, style=self.style.child(font=(self.style.font, 25)), padx=200, pady=28) \
			.inline_bind('<MouseWheel>', self.vol_change_e) \
			.inline_pack()

		tmp = (3, 1) if self.ut.config['switch_controls'] else (1, 3)
		for b in [
			(f'<Button-{tmp[0]}>', lambda e: self.ut.next_song() or self.stage.switch('')),
			(f'<Button-{tmp[1]}>', lambda e: self.ut.next_song(-1) or self.stage.switch(''))
		]:
			self.l_volume.bind(*b)

	def activate(self):
		self.timer = datetime.now()
		self.l_volume.set_(self.ut.player.get_volume())
		self.l_volume.config(fg=self.l_volume.style.fg)
		super().activate()

	def typed(self, event) -> None:
		if event.keysym == 'Escape':
			self.stage.switch('')

	def tick(self):
		b = self.winfo_rgb(self.style.bg)
		f = self.winfo_rgb(self.style.fg)
		p = 1 - round((datetime.now() - self.timer).total_seconds() / Volume.COUNTDOWN, 3)
		self.l_volume.config(fg='#' + ''.join([format(int((b[i] + (f[i] - b[i]) * min(p + 0.1, 1)) / 256), 'x').zfill(2) for i in range(3)]))
		if p <= 0:
			self.stage.switch('')

	def vol_change_e(self, event):
		self.timer = datetime.now()
		a = int(self.ut.player.get_volume() + event.delta / 120)
		self.ut.player.set_volume(a)
		if a > 100:
			self.ut.stats.set(self.ut.stats.events.h_volume_max, 1)
		self.master.after(2)
		self.l_volume.set_(self.ut.player.get_volume())
