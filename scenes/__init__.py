from scenes import main


class ScenesManager:
	def __init__(self, root, utano, theme):
		self._root_ = root
		self._ut_ = utano
		self._theme_ = theme

		self.s_main = main.Main(self._root_, self._ut_, self._theme_)

		self.activated: main.Scene = main.Scene()
		self.switch(self.s_main)

	def tick(self):
		self.activated.tick()

	def switch(self, to: main.Scene):
		self.activated.deactivate()
		self.activated = to
		self.activated.activate()
