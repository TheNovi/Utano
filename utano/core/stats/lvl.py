class Lvl:
	def __init__(self, lvl=1, exp=0, method=lambda lvl: 2 ** lvl, popup: callable = None):
		self._lvl = lvl
		self._exp = exp
		self.method = method
		self.popup = popup

	@property
	def exp(self):
		return self._exp

	def add_exp(self, value):
		self._exp += max(0, value)
		self._check()

	@property
	def lvl(self):
		return self._lvl

	def _check(self):
		while self.exp_to_next_lvl() <= 0:
			self._exp -= self.total_exp_to_next_lvl()
			self._lvl += 1
			if self.popup:
				self.popup(self)

	def total_exp_to_next_lvl(self):
		return self.method(self._lvl)

	def exp_to_next_lvl(self):
		return self.total_exp_to_next_lvl() - self.exp

	def __repr__(self) -> str:
		return f"<Nlvl: lvl: {self._lvl}, exp: {self.exp}, total_next: {self.total_exp_to_next_lvl()}>"

	def save(self) -> dict:
		return {'l': self._lvl, 'e': self._exp}

	def load(self, d: dict):
		self._lvl = d.get('l', self._lvl)
		self._exp = d.get('e', self._exp)
		return self
