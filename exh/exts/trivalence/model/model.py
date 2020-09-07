import numpy as np

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


	def create_assignment(self):
		""" Overriding same method from base class ; creates trivalent assignment. """
		return utils.get_many_valued_assignment(self.n) - 1

	def __init__(self, **kwargs):
		"""
		Keyword arguments:
		f  -- one formula from which to extract the predicates
		vm -- a variable manager object
		fs -- a list of formulas from which to ex
		"""
		super(Universe, self).__init__(**kwargs)

	def update(self, var):
		self.vm     = VarManager.merge(self.vm, var.vm)
		self.n      = self.vm.n
		self.worlds = self.create_assignment()


	def consistent(self, *fs):
		"""
		In a trivalent setting, this returns True if there is a world in which all formulas are true
		(Note this yields a bivalent result)
		"""
		output = self.evaluate(*fs)
		return np.any(np.all(output == TVal.true, axis = 1)) 

	def format_row(self, row):
		"""
		Format row in truth table with names from TVal class
		"""
		return [TVal(cell).name for cell in row]