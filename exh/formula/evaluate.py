import numpy as np
import itertools

import exh.utils as utils
from . import options as formula_options

### EVALUATION METHODS ###			

class Evaluate:
	"""
	Evaluate the formula with respect to an assignment of values to the propositional and predicate variable

	Arguments:
		- vm (optional, default = self.vm) : a variable manager for the variables in the formula
		either
			- assignment : a boolean numpy array ; at index i, is the value for the independent variable with index i according to vm
		or
			- kwargs : a dictionary ; for every key, provides the value of the propositional or predicate variable with that name
				if proposition, the value must be boolean
				if n-ary predicate, value must be a boolean numpy array with size (formula_options.dom_quant)^n
	"""
	def evaluate(self, **kwargs):

		if "vm" in kwargs:
			vm = kwargs["vm"]
		else: 
			vm = self.vm

		# If assignment is provided, use it ; otherwise, construct one from keyword arguments
		if "assignment" in kwargs:
			assignment = kwargs["assignment"]
		else:
			assignment = np.full(vm.n, True)

			for var, val in kwargs.items():
				if var in vm.names:
					idx = vm.names[var]
				else:
					continue

				deps = vm.preds[idx]

				for t in itertools.product(range(formula_options.dom_quant), repeat = deps):
					i = vm.index(idx, t)
					assignment[i] = utils.get(val, t)

			assignment = assignment[np.newaxis, :]


		to_return = self.evaluate_aux(assignment, vm)

		if all(dim == 1 for dim in to_return.shape):
			return np.asscalar(to_return)
		else:
			return to_return


	def evaluate_aux(self, assignment, vm, variables = dict()):
		raise Exception("evaluate_aux has not been implemented for the current type of formula")


		if self.type == "and":
			return np.min(np.stack([child.evaluate_aux(assignment, vm, variables) for child in self.children]), axis = 0)
		elif self.type == "or":
			return np.max(np.stack([child.evaluate_aux(assignment, vm, variables) for child in self.children]), axis = 0)
		elif self.type == "not":
			return np.logical_not(self.children[0].evaluate_aux(assignment, vm, variables))



