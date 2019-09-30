from scenes import main, volume, catalog, stats, achieve, notification


class ScenesManager:
	def __init__(self, root, utano, theme):
		self.root = root
		self.ut = utano
		self.theme = theme

		self.notifications = []

		args = (self.root, self, self.ut, self.theme)
		self.s_main = main.Main(*args)
		self.s_volume = volume.Volume(*args)
		self.s_catalog = catalog.Catalog(*args)
		self.s_stats = stats.Stats(*args)
		self.s_achieve = achieve.Achieve(*args)
		# noinspection PyTypeChecker
		self.activated: main.Scene = type("TypeScene", (), {'deactivate': lambda: None})

		self.root.bind('<Escape>', self.escape)
		self.root.bind('<Key>', self.typed)

		self.s_main.switch_to_me()

	def tick(self):
		self.activated.tick()
		for n in self.notifications:
			if n.tick():
				n.destroy()
				self.notifications.remove(n)

	def typed(self, event):
		if event.keysym in ['Up', 'Left', 'Down', 'Right']:
			self.activated.typed(event)
		elif len(event.keysym) == 1 and self.activated in [self.s_main, self.s_volume]:
			self.s_catalog.switch_to_me()
			self.s_catalog.e_search.insert(0, event.char)

	def switch(self, to: main.Scene):
		self.activated.deactivate()
		self.activated = to
		self.activated.activate()

	def escape(self, *_, **__):
		self.s_main.switch_to_me()

	def achieve_call(self, achievement):
		self.show_notification()
		self.s_achieve.pack_achieve(achievement, self.notifications[-1])

	def show_notification(self, time: int = 5):
		self.notifications.append(notification.Notification(self.root, self, self.ut, self.theme).activate(time))
