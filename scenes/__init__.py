from scenes import main, volume, catalog


class ScenesManager:
	def __init__(self, root, utano, theme):
		self._root_ = root
		self._ut_ = utano
		self._theme_ = theme

		args = (self._root_, self, self._ut_, self._theme_)
		self.s_main = main.Main(*args)
		self.s_volume = volume.Volume(*args)
		self.s_catalog = catalog.Catalog(*args)
		# noinspection PyTypeChecker
		self.activated: main.Scene = type("TypeScene", (), {'deactivate': lambda: None})

		self._root_.bind('<Escape>', self.escape)
		for t in ['Up', 'Left', 'Down', 'Right']:
			self._root_.bind(f'<{t}>', self.typed)

		self.s_main.switch_to_me()

	def tick(self):
		self.activated.tick()

	def typed(self, event):
		self.activated.typed(event)

	def switch(self, to: main.Scene):
		self.activated.deactivate()
		self.activated = to
		self.activated.activate()

	def escape(self, *_, **__):
		self.s_main.switch_to_me()
