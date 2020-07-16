from core import Utano
from . import catalog, gue_main, mod_changer
from . import main, volume, select, stats, achieve, notification


class ScenesManager:
	def __init__(self, root, utano: Utano, theme):
		self.root = root
		self.utano: Utano = utano
		self.theme = theme

		self.notifications = []
		self.mod = 0  # 0-main, 1-gue

		args = (self.root, self, self.utano, self.theme)
		self.s_main = main.Main(*args)
		self.s_volume = volume.Volume(*args)
		self.s_select = select.Select(*args)
		self.s_catalog = catalog.Catalog(*args)
		self.s_stats = stats.Stats(*args)
		self.s_achieve = achieve.Achieve(*args)

		self.gue_main = gue_main.Main(*args)

		self.mod_changer = mod_changer.ModChanger(*args)
		# noinspection PyTypeChecker
		self.activated: main.Scene = type("TypeScene", (), {'deactivate': lambda: None})

		self.root.bind('<Escape>', self.escape)
		self.root.bind('<Key>', self.typed)

		self.s_main.activate_mod()

	def tick(self):
		self.activated.tick()
		for n in self.notifications:
			if n.tick():
				n.destroy()
				self.notifications.remove(n)

	def typed(self, event):
		if event.keysym in ['Up', 'Left', 'Down', 'Right']:
			self.activated.typed(event)
		elif self.mod == 0 and len(event.keysym) == 1 and self.activated in [self.s_main, self.s_volume]:
			self.s_catalog.switch_to_me()
			self.s_catalog.e_search.insert(0, event.char)

	def switch(self, to: main.Scene):
		self.activated.deactivate()
		self.activated = to
		self.activated.activate()
		self.activated.focus_set()

	def escape(self, *_, **__):
		if self.mod == 0:
			self.s_main.switch_to_me()
		elif self.mod == 1:
			self.gue_main.switch_to_me()

	def next_song_call(self):
		if self.mod == 0:
			self.s_main.next_song_call()

	# elif self.mod == 1:
	# 	self.gue_main.next_song_call()

	def achieve_call(self, achievement):
		self.show_notification()
		self.s_achieve.pack_achieve(achievement, self.notifications[-1])

	def show_notification(self, time: int = 5):
		self.notifications.append(notification.Notification(self.root, self, self.utano, self.theme).activate(time))
