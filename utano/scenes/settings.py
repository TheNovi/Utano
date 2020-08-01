from nui.gui.v1 import Scene, Stage

from core import Utano


class Settings(Scene):
	def __init__(self, stage: Stage, ut: Utano):
		super().__init__(stage)
		self.ut = ut
