import exh.model as model
import exh.exts.trivalence.utils as utils
from exh.exts.trivalence.model.truth import TVal

class Universe(model.Universe):
	"""
	Trivalent counterpart to model.Universe. Each world gives one of three truth values to predicates and propositions: true, false and pound

	Subtelties:
		* method "entails"    gives Strawson-entailment
		* method "consistent" gives true iff some world makes all formulas true
	"""
	def __init__(self, **kwargs):
		if "worlds" not in kwargs:
			kwargs["worlds"] = utils.get_many_valued_assignment(n) - 1 # the assignment has values between 0 and 2 ; -1 to bring them to the range [-1,0,1]

		super(Universe, self).__init__(**kwargs)

	def update(self, var):
		self.vm     = VarManager.merge(self.vm, var.vm)
		self.n      = self.vm.n
		self.worlds = utils.get_many_valued_assignment(n) - 1


	def consistent(self, *fs):
		"""
		In a trivalent setting, this returns True if there is a world in which all formulas are true
		(Note this yields a bivalent result)
		"""
		output = self.evaluate(*fs)
		return np.max(np.min(TVal.swap(output), axis = 1)) == TVal.true

	def format_row(self, row):
		"""
		Format row in truth table with names from TVal class
		"""
		return [TVal(row).name for cell in row]