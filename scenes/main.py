import tkinter
from utano import Utano


class Main(tkinter.Frame):
	def __init__(self, master, ut: Utano, theme, **kw):
		super().__init__(master, bg=theme['bg'], **kw)
		self.ut = ut
		self.s_name = tkinter.StringVar()
		self.s_artist = tkinter.StringVar()
		self.l_name = tkinter.Label(self, textvariable=self.s_name, bg=theme["bg"], fg=theme['fg'], font=(theme['font'], 25))
		self.l_artist = tkinter.Label(self, textvariable=self.s_artist, bg=theme['bg'], fg=theme['fg'], font=(theme['font'], 15))
		self.song_line = tkinter.Label(self, bg=theme['bg'], fg=theme['fg'], font=('helvetica', 5))

		self.l_name.pack(fill='both')
		self.l_artist.pack(fill='both')
		self.song_line.pack(fill='both')
		self.l_name.bind("<Button-1>", lambda e: self.ut.next_song())
		self.l_name.bind("<Button-3>", lambda e: self.ut.next_song(-1))
		self.l_artist.bind("<Button-1>", lambda e: self.ut.next_song())
		self.l_artist.bind("<Button-3>", lambda e: self.ut.next_song(-1))

	def tick(self):
		self.u_song_line()

	def u_song_line(self):
		p = (1 - self.ut.player.p.get_position())
		p = min(1, max(0, p))
		self.song_line['text'] = '-' * int(p * self.song_line.winfo_width()/2.3)

	def next_song_call(self):
		s = self.ut.get_actual_song()
		self.s_name.set(s.name)
		self.s_artist.set(s.artist)
