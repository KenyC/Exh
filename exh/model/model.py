import numpy as np
import itertools

from . import options
import exh.utils as utils
from .vars import VarManager
from exh.utils.table import Table
# from formula import Var

class Universe:
	"""	
	Universe generates a set of assignments of truth-values for every predicate (i.e. a world).
	The assigments either cover all the logical space.or just some logical possibilities

	Attributes:
	n      -- number of bits that specify the world (example: propositional varaible a requires 1 bit, unary predicates a(x) as many bits as there are individuaks)
	worlds -- numpy boolean array worlds[i, j] specifies the truth-value of the j-th bit at the i-th world
	vm     -- variable manager ; specifies a mapping from predicates to bit position (example: predicate variable "a" is mapped to "x")
	
	Properties:
	n_worlds -- number of worlds in universe
	"""

	def __init__(self, **kwargs):
		"""
		Keyword arguments:
		f  -- one formula from which to extract the predicates
		vm -- a variable manager object
		fs -- a list of formulas from which to ex
		"""
		
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
		"""Checks if f1 entails f2 in universe"""
		return not self.consistent(f1 & ~f2)

	def equivalent(self, f1, f2):
		output = self.evaluate(f1, f2)
		return np.all(output[:, 0] == output[:, 1])

	def evaluate(self, *fs, **kwargs):
		"""
		Evaluate formules against every world in universe
		"""

		return np.transpose(np.stack([f.evaluate(assignment = self.worlds, vm = self.vm, **kwargs) for f in fs]))


	def name_worlds(self):
		"""
		Returns list of meaningful names to bits, depending on which predicates they set true

		e.g. if Universe is for propositional variable "a", and unary predicate "b" will return
		["a", "b(0)", "b(1)", "b(2)"]
		"""

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
		"""Returns Universe object restricted to the worlds with indices in "indices" argument"""

		return Universe(vm = self.vm, worlds = self.worlds[indices])


	def update(self, var):
		self.vm = VarManager.merge(self.vm, var.vm)
		self.n = self.vm.n
		self.worlds = utils.getAssignment(n)

	def truth_table(self, *fs, **kwargs):
		"""Display a truth-table for formulas fs. Keyword arguments are passed to table (cf exh.utils.table)"""

		output = self.evaluate(*fs)

		table = Table(**kwargs)
		nvars = self.worlds.shape[1]
		nworlds = self.worlds.shape[0]

		# We find the names for the columns
		name_cols = self.name_worlds() + [str(f) for f in fs]
		table.set_header(name_cols)

		# self.worlds: nworlds x nvars
		# output : nworlds x nfs
		combined = np.concatenate([self.worlds, output], axis = 1)

		for row in combined:
			table.add_row(row)

		table.set_strong_col(nvars)
		table.print()	




