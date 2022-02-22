class Posting:
	def __init__(self, name: str = None, freq: int = None) -> None:
		self.name = name
		self.freq = freq

	def getName(self) -> str:
		return self.name

	def getFreq(self) -> str:
		return self.freq

	def __repr__(self) -> str:
		return f"Posting({self.name}, {self.freq})"	

	def __str__(self) -> str:
		return f"file: {self.name} - freq: {self.freq}"	
	