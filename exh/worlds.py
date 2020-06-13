import numpy as np
import itertools

import exh.options as options
import exh.utils as utils
from exh.vars import VarManager
from exh.table import Table
# from formula import Var

"""
Universe generates a set of worlds for a formula, a set of formulas, or an index
"""
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
			self.worlds = utils.getAssignment(self.n)
		else:
			self.worlds = kwargs["worlds"]

	@property
	def n_worlds(self):
		return self.worlds.shape[0]
	

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


	""" 
	Gives meaningful names to worlds, depending on which predicates they set
	"""
	def name_worlds(self):

		def str_tuple(tuple):
			return "({})".format(",".join(list(map(str, t))))
			
		nvars = self.worlds.shape[1]
		names = [i for i in range(nvars)]
		name_vars = ["A{}".format(key) for key in self.vm.preds.keys()]

		for name, var_idx in self.vm.names.items():
			vm_index = self.vm.pred_to_vm_index[var_idx]
			name_vars[vm_index] = name

		vm_idx_to_deps = list(self.vm.preds.values())

		for i, offset in enumerate(self.vm.offset):
			ndeps = vm_idx_to_deps[i]
			
			if ndeps != 0:
			
				for t in itertools.product(range(options.dom_quant), repeat = ndeps):
					i_col = offset + sum(val * options.dom_quant ** j for j, val in enumerate(t))
					names[i_col] = name_vars[i] + str_tuple(t)

			else:
				names[offset] = name_vars[i]

		return names


	

	

	def restrict(self, indices):
		return Universe(vm = self.vm, worlds = self.worlds[indices])


	def update(self, var):
		self.vm = VarManager.merge(self.vm, var.vm)
		self.n = self.vm.n
		self.worlds = utils.getAssignment(n)

	def truth_table(self, *fs):


		output = self.evaluate(*fs)

		table = Table()
		nvars = self.worlds.shape[1]
		nworlds = self.worlds.shape[0]

		# We find the names for the columns
		name_cols = self.name_worlds() + [str(f) for f in fs]
		# name_vars = ["A{}".format(key) for key in self.vm.preds.keys()]
		# for name, var_idx in self.vm.names.items():
		# 	vm_index = self.vm.pred_to_vm_index[var_idx]
		# 	name_vars[vm_index] = name

		# vm_idx_to_deps = list(self.vm.preds.values())

		# for i, offset in enumerate(self.vm.offset):
		# 	ndeps = vm_idx_to_deps[i]
			
		# 	if ndeps != 0:
			
		# 		for t in itertools.product(range(options.dom_quant), repeat = ndeps):
		# 			i_col = offset + sum(val * options.dom_quant ** j for j, val in enumerate(t))
		# 			name_cols[i_col] = name_vars[i] + str_tuple(t)

		# 	else:
		# 		name_cols[offset] = name_vars[i]


		table.set_header(name_cols)

		# self.worlds: nworlds x nvars
		# output : nworlds x nfs
		combined = np.concatenate([self.worlds, output], axis = 1)

		for row in combined:
			table.add_row(row)

		table.set_strong_col(nvars)
		table.print()	




