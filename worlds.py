import numpy as np
import itertools

from options import *
from assignment import getAssignment
from vars import VarManager
# from formula import Var


class Universe:

	def __init__(self, **kwargs):
		
		if "f" in kwargs:
			self.vm = kwargs["f"].vm
		elif "vm" in kwargs:
			self.vm = kwargs["vm"] 
		elif "fs" in kwargs:
			self.vm = VarManager.merge(*[f.vm for f in kwargs["fs"]])

		self.n = self.vm.n

		if "worlds" not in kwargs:
			self.worlds = getAssignment(self.n)
		else:
			self.worlds = kwargs["worlds"]

	def consistent(self, *fs):

		output = self.evaluate(*fs)

		return np.any(np.min(output, axis = 1))

	# def set(pred, value, **variables):
	# 	if isinstance(pred, Var):
	# 		idx = pred.idx
	# 	else:
	# 		idx = pred

	# 	deps = self.vm.preds[idx]

	# 	# Variables for which no value has been provided
	# 	no_val_vars = list(set(deps.keys()) - set(variables.keys()))
		
	# 	def all_vars_assignment():
	# 		for vals in product(range(options.dom_quant), repeat = len(no_val_vars)):
	# 			d = {var: val for var, val in zip(no_val_vars, vals)}
	# 			d.update(variables)
	# 			yield d


	# 	ko_cols = [self.vm.index(idx, **d) for d in iterator()]

	# 	# We remove all the lines where the values of column does not match value
	# 	reduced_worlds = self.u.worlds[:, ko_cols]
	# 	goal = np.full_like(reduced_worlds, value)

	# 	indices_keep = np.max((goal == reduced_worlds), axis = 1)

	# 	self.worlds = self.worlds[indices_keep, :]


	def entails(self, f1, f2):
		return not self.consistent(f1 & ~f2)

	def equivalent(self, f1, f2):
		output = self.evaluate(f1, f2)
		return np.all(output[:, 0] == output[:, 1])

	def evaluate(self, *fs):
		return np.transpose(np.stack([f.evaluate(assignment = self.worlds, vm = self.vm) for f in fs]))

	def restrict(self, indices):
		return Universe(vm = self.vm, worlds = self.worlds[indices])

	def update(self, var):
		self.vm = VarManager.merge(self.vm, var.vm)
		self.n = self.vm.n
		self.worlds = getAssignment(n)
