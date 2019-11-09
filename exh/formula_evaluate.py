import numpy as np
import itertools

import exh.utils as utils
import exh.options as options

### EVALUATION METHODS ###			

def evaluate(self, **kwargs):

	if "vm" in kwargs:
		vm = kwargs["vm"]
	else: 
		vm = self.vm


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

			for t in itertools.product(range(options.dom_quant), repeat = len(deps)):
				i = vm.index(idx, **{key: val for key, val in zip(deps, t)})
				assignment[i] = utils.get(val, t)

		assignment = assignment[np.newaxis, :]


	to_return = self.evaluate_aux(assignment, vm)

	if all(dim == 1 for dim in to_return.shape):
		return np.asscalar(to_return)
	else:
		return to_return


def evaluate_aux(self, assignment, vm, variables = dict()):


	if self.type == "and":
		return np.min(np.stack([child.evaluate_aux(assignment, vm, variables) for child in self.children]), axis = 0)
	elif self.type == "or":
		return np.max(np.stack([child.evaluate_aux(assignment, vm, variables) for child in self.children]), axis = 0)
	elif self.type == "not":
		return np.logical_not(self.children[0].evaluate_aux(assignment, vm, variables))

	raise Exception("evaluate_aux has not been implemented for the current type of formula")


methods = [evaluate, evaluate_aux]