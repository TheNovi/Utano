from typing import Dict

from nui.gui.v1 import Scene, Stage, Label, Frame

from core import Utano


class Achievements(Scene):
	def __init__(self, stage: Stage, ut: Utano):
		super().__init__(stage)
		self.ut: Utano = ut
		Label(self, text="Achievements", style=self.style.child(font=(self.style.font, 10))).inline_pack()
		Label(self, text=12 * '----------', style=self.style.child(font=('helvetica', 5))).inline_pack()
		self.frame = Frame(self)

	def activate(self) -> None:
		self.frame.destroy()
		self.frame = Frame(self).inline_pack()
		groups: Dict[str, Frame] = {}
		for a in self.ut.stats.achievements:  # TODO Better handler for group=0
			f = groups.get(a.group, None)
			if not f:
				f = Frame(self.frame).inline_pack()
				groups[a.group] = f
			f = Frame(f, highlightthickness=1, highlightbackground='#660000')  # TODO Style color
			fg = self.style.fg if a.got else '#880000'
			if a.got:
				Label(f, text=a.name + '  ', anchor='w', pady=0, style=self.style.child(font=(self.style.font, 10), fg='White')).pack(fill='both', pady=0)
			Label(f, text=a.desc, anchor='w', pady=0, style=self.style.child(font=(self.style.font, 8), fg=fg)).pack(fill='both', pady=0, expand=True)
			# if not a.got and a.count - 1: #NOSONAR TODO
			# 	Label(f, text=f"{min([self.ut.stats.values.get(a.event.name, 0), a.count])}/{a.count}  {int(min([self.utano.stats.values.get(a.event.name, 0), a.count]) * 100 / a.count)}%", bg='Black', fg=fg, anchor='e', pady=0, font=('helvetica', 7)).pack(fill='both', pady=0)
			f.pack(fill="both", side='left', expand=True)
		super().activate()
