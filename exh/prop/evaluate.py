import numpy as np
import itertools

import exh.utils as utils
import exh.model.options as options

### EVALUATION METHODS ###			

class Evaluate:
	
	def evaluate(self, **kwargs):
		"""
		Evaluate the formula with respect to an assignment of values to the propositional and predicate variable

		Arguments:
			vm (VarManager, default = self.vm) -- a variable manager for the variables in the formula
			either
				assignment (np.ndarray[bool]) -- at index i, is the value for the independent variable with index i according to vm
			or
				kwargs (dict) -- for every key, provides the value of the propositional or predicate variable with that name
					if proposition, the value must be boolean
					if n-ary predicate, value must be a boolean numpy array with size (options.dom_quant)^n
			no_flattening (bool, default = False) -- prevent automatic flattening of result if the result is one-dimensional

		Returns:
			np.ndarray[bool] -- Boolean array of shape (n_assignment, dom_quant, ..., dom_quant) specifying for each assignment and values given to free variables
			                                                         <---number of free vars-->
		or 
			bool -- if the latter result is single dimensional
		"""

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

				for t in itertools.product(range(options.dom_quant), repeat = deps):
					i = vm.index(idx, t)
					assignment[i] = utils.get(val, t)

			assignment = assignment[np.newaxis, :]

		variables = kwargs.get("variables", dict())
		free_vars = [var for var in kwargs.get("free_vars", self.free_vars) if var not in variables]
		to_return = self.evaluate_aux(assignment, vm, variables = variables, free_vars = free_vars)

		if all(dim == 1 for dim in to_return.shape) and not ("no_flattening" in kwargs and kwargs["no_flattening"]):
			return np.asscalar(to_return)
		else:
			return to_return


	def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):
		"""
		Auxiliary method for recursion ; evaluates sub-formula (to be overridden by children classes)
		
		Arguments:
			assignment (numpy.ndarray[bool]) -- each line specifies a different assignmen of bit positions to truth values # TODO: rename to worlds
			vm         (VariableManager)     -- variable manager mapping predicate and variable names to bit positions
			variables  (dict[str, int])      -- local assignment of values to variables
			free_vars  (list[str])           -- variables left free in the matrix formula (the formula on which "evaluate" was called)
		
		Returns:
		   np.ndarray[bool] -- Boolean array of shape (n_assignment, dom_quant, ..., dom_quant) specifying for each assignment and values given to free variables
		                                                             <---number of free vars-->
		"""
		raise Exception("evaluate_aux is not been implemented for class {}".format(self.__class__.__name__))




