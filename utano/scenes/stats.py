from datetime import timedelta
from typing import Callable, Any

from nui.gui.v1 import Scene, Stage, Label, Frame

from core import Utano


class Stats(Scene):
	def __init__(self, stage: Stage, ut: Utano):
		super().__init__(stage)
		self.ut: Utano = ut
		Label(self, text="Your statistics", style=self.style.child(font=(self.style.font, 10))).inline_pack()
		Label(self, text=12 * '----------', style=self.style.child(font=('helvetica', 5))).inline_pack()
		self.f_stats = Frame(self)

	def activate(self, whisper=None) -> None:
		self.f_stats.destroy()
		self.f_stats = Frame(self)
		m = self.f_stats
		s = self.ut.stats
		self.stat(m, 'Stats Created', s.stats_created)
		self.stat(m, 'Program Started', s.program_started)
		self.stat(m, 'Song Played', s.song_played)
		self.stat(m, 'Song Skipped', s.song_skipped)
		self.stat(m, 'Paused', s.paused)
		self.stat(m, 'Song Replayed', s.song_replayed)
		self.stat(m, 'Song Selected', s.song_selected)
		self.stat(m, 'Playlist Completed', s.playlist_completed)
		self.stat(m, 'Total Time', s.total_time, lambda v: str(timedelta(seconds=v + int(self.ut.get_time() / 1000))).split('.')[0])
		self.f_stats.inline_pack()
		super().activate()

	@staticmethod
	def stat(master: Frame, name: str, stat, parser: Callable[[Any], str] = lambda v: v):
		s = master.style.child(font=(master.style.font, 10), bg=master.style.bg if len(master.winfo_children()) % 2 else '#333333')  # TODO Do dynamic second color
		o = Frame(master, style=s)
		Label(o, style=s, text=name + ': ', anchor='w').pack(fill='x', side='left')
		Label(o, style=s, text=parser(stat.value), anchor='e').pack(fill='x', side='right', expand=True)
		o.inline_pack()

	def typed(self, event):
		if event.keysym in ['Escape', 'Left']:
			self.stage.switch('')
		elif event.keysym == 'Down':
			self.stage.switch('c')
		elif event.keysym == 'Right':
			self.stage.switch('a')
