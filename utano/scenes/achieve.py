import tkinter

from .scene import Scene


# noinspection PyAttributeOutsideInit
class Achieve(Scene):  # TODO Better colors
	def _init_(self):
		super()._init_()
		self.l_title = tkinter.Label(self, text="Achievements", bg=self.theme["bg"], fg=self.theme['fg'], font=(self.theme['font'], 10))
		self.l_line = tkinter.Label(self, text=12 * '----------', bg=self.theme["bg"], fg=self.theme['fg'], font=('helvetica', 5))
		self.f_achieve = tkinter.Frame(self)

		self.l_title.pack(fill='both')
		self.l_line.pack(fill='both')

	def activate(self):
		super().activate()
		c = len([x for x in self.utano.stats.achieve if x.got_it])
		self.l_title['text'] = f"Achievements {c}/{len(self.utano.stats.achieve)} {int(c * 100 / len(self.utano.stats.achieve))}%"

		self.f_achieve.destroy()
		self.f_achieve = tkinter.Frame(self)
		self.f_achieve.pack(fill='both')

		bef = self.utano.stats.achieve[0].event
		packed = False
		f = tkinter.Frame(self.f_achieve)
		for a in self.utano.stats.achieve:
			if a.event.name.startswith('h_'):
				break
			if a.event != bef:
				packed = False
				f.pack(fill='both')
				f = tkinter.Frame(self.f_achieve)
				bef = a.event
			if not packed:
				self.pack_achieve(a, f)
				if not a.got_it:
					f.pack(fill='both')
					packed = True
			else:
				tkinter.Label(f, bg=self.theme['bg'], font=(self.theme['font'], 10)).pack(fill='both', side='left', expand=True)
		f.pack(fill='both')
		f = tkinter.Frame(self.f_achieve)
		[self.pack_achieve(x, f) for x in self.utano.stats.achieve if x.event.name.startswith('h_') and not x.desc.startswith('h_')]
		[self.pack_achieve(x, f) for x in self.utano.stats.achieve if x.got_it and x.desc.startswith('h_')]
		if f.winfo_children():
			f.pack(fill='both')
		else:
			f.destroy()

	def pack_achieve(self, a, frame):
		f = tkinter.Frame(frame, highlightthickness=1, highlightbackground='#660000')
		fg = self.theme['fg'] if a.got_it else '#880000'
		if a.got_it:
			tkinter.Label(f, text=a.name + '  ', bg=self.theme['bg'], fg='White', anchor='w', pady=0, font=(self.theme['font'], 10)).pack(fill='both', pady=0)
		tkinter.Label(f, text=a.desc.replace('h_', ''), bg=self.theme['bg'], fg=fg, anchor='w', pady=0, font=(self.theme['font'], 8)).pack(fill='both', pady=0, expand=True)
		if not a.got_it and a.count - 1:
			tkinter.Label(f, text=f"{min([self.utano.stats.values.get(a.event.name, 0), a.count])}/{a.count}  {int(min([self.utano.stats.values.get(a.event.name, 0), a.count]) * 100 / a.count)}%", bg='Black', fg=fg, anchor='e', pady=0, font=('helvetica', 7)).pack(fill='both', pady=0)
		f.pack(fill="both", side='left', expand=True)

	def typed(self, event):
		super().typed(event)
		super().typed(event)
		if event.keysym == 'Down':
			self.manager.s_catalog.switch_to_me()
		elif event.keysym == 'Up':
			self.manager.s_volume.switch_to_me()
		elif event.keysym == 'Left':
			self.manager.s_stats.switch_to_me()
		elif event.keysym == 'Right':
			self.manager.escape()
