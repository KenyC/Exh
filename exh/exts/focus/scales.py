from exh.exts.focus.formula import Focus
from exh.scales import Scales

class FocusScales(Scales):
	"""docstring for FocusScales"""
	def __init__(self):
		super(FocusScales, self).__init__()

	def alternatives_to(self, prejacents):
		"""
		From a list of prejacents assumed to have the same root operator Op
		"""
		return [
			alt 
			for prejacent in prejacents 
			if isinstance(prejacent, Focus) 
			for alt in prejacent.alts
		]						

