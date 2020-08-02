from nui.gui.v1 import Scene, Stage, Label, Form, Entry, Button
from nui.gui.v1.widgets.toggle import Toggle

from core import Utano


class Settings(Scene):
	def __init__(self, stage: Stage, ut: Utano):
		super().__init__(stage)
		self.ut = ut
		self.style = self.style.child(font=(self.style.font, 10))
		Label(self, text="Settings").inline_pack()
		Label(self, text=30 * '----------', style=self.style.child(font=('helvetica', 5))).inline_pack()
		spacing = ':' + 5 * ' '
		self.form = Form(self) \
			.add_field('music_path', Entry, 'Music path' + spacing, lambda: self.ut.config.music_path) \
			.add_field('raw_theme_path', Entry, 'Theme path' + spacing, lambda: self.ut.config.raw_theme_path) \
			.add_field('raw_stats_path', Entry, 'Stats path' + spacing, lambda: self.ut.config.raw_stats_path) \
			.add_field('raw_lrc_path', Entry, 'Lrc path' + spacing, lambda: self.ut.config.raw_lrc_path) \
			.add_field('volume', Entry, 'Volume' + spacing, lambda: self.ut.config.volume) \
			.add_field('replay_when_progress', Entry, 'Replay when progress' + spacing, lambda: self.ut.config.replay_when_progress) \
			.add_field('start_paused', Toggle, 'Start paused' + spacing, lambda: self.ut.config.start_paused) \
			.add_field('auto_play', Toggle, 'Auto play' + spacing, lambda: self.ut.config.auto_play) \
			.add_field('disable_stop_button', Toggle, 'Disable stop button' + spacing, lambda: self.ut.config.disable_stop_button) \
			.add_field('switch_controls', Toggle, 'Switch controls' + spacing, lambda: self.ut.config.switch_controls) \
			.add_field('reverse_title', Toggle, 'Reverse title' + spacing, lambda: self.ut.config.reverse_title) \
			.add_field('reverse_in_list', Toggle, 'Reverse in list' + spacing, lambda: self.ut.config.reverse_in_list) \
			.inline_pack()
		Button(self, self.write, 'Save').inline_pack()

	def activate(self) -> None:
		self.form.set_fields()
		super().activate()

	def write(self):
		self.ut.config.music_path = self.form['music_path']
		self.ut.config.raw_theme_path = self.form['raw_theme_path']
		self.ut.config.raw_stats_path = self.form['raw_stats_path']
		self.ut.config.raw_lrc_path = self.form['raw_lrc_path']
		try:
			self.ut.config.volume = int(self.form['volume'])
		except Exception:
			pass
		try:
			self.ut.config.replay_when_progress = int(self.form['replay_when_progress'])
		except Exception:
			pass
		self.ut.config.start_paused = self.form['start_paused']
		self.ut.config.auto_play = self.form['auto_play']
		self.ut.config.disable_stop_button = self.form['disable_stop_button']
		self.ut.config.switch_controls = self.form['switch_controls']
		self.ut.config.reverse_title = self.form['reverse_title']
		self.ut.config.reverse_in_list = self.form['reverse_in_list']

	def typed(self, event):
		if event.keysym in ['Escape', 'Down']:
			self.stage.switch('')
