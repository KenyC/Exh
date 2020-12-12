import numpy as np
from . import options
from . import exceptions

class Domain:
	"""
	Represents some domain of quantification. 

	Attributes:
		- n (int) -- the size of the domain of quantification
	"""
	def __init__(self, size):
		self._n = size

	@property
	def n(self):
		return self._n
	


class DefaultDomain(Domain):
	"""
	A domain whose size is rigidly bound to "options.dom_quant"
	"""
	def __init__(self):
		super(DefaultDomain, self).__init__(options.dom_quant)

	@property
	def n(self):
		return options.dom_quant
	
default_domain = DefaultDomain()


class VarManager:
	"""
	VarManager keeps track of all independent variables in a given system.
	Maps propositional variables and fully saturated predicate variables to indices

	Example: 
	System: unary predicate p and proposition q; domain of individuals = 3
	Values: p(0) p(1) p(2) q
	are mapped to
	Indices: 0    1    2   3
	
	Attributes:
		preds             -- a dictionary mapping predicate indices to the sizes of the domains they depend on
		pred_to_vm_index  -- a dictionary mapping predicate indices to a position (e.g. if a has index 1 and b index 4, a is mapped to position 0 and b to position 1)
		names             -- a dictionary mapping predicate names to their indices 
		memory            -- a list mapping predicate positions to how many bits are required to define this predicate
		offset            -- a list mapping predicate positions to the bit index offset at which they are defined.
	"""
	def __init__(self, preds, names = dict()):
		self.preds = preds 
		self.names = names

		# pred_to_vm_index : dictionary mapping Formula's predicate indices to VarManager's predicate indices
		self.pred_to_vm_index = {pred_idx: vm_idx for vm_idx, pred_idx in enumerate(self.preds.keys())}
		self.linearize()

	def linearize(self):
		"""
		How many independent boolean values to specify the propositional variables.

		propositions: 1 i
		unary predicate: dom_quant
		etc
		"""

		self.memory = [grand_product(deps)  for _, deps in self.preds.items()]
		
		# position in memory of bits devoted to a parcitular predicate
		self.offset = [0]
		for mem in self.memory[:-1]:
			self.offset.append(self.offset[-1] + mem)

	def merge(*vms):
		return VarManager(preds = {k: v for vm in vms for k, v in vm.preds.items()},
						  names = {k: v for vm in vms for k, v in vm.names.items()})

	@property
	def n(self):
		"""
		Number of bits required to specify an assignment 
		"""
		return sum(self.memory)

	def index(self, pred, value_slots):
		if pred in self.preds:
			deps = self.preds[pred]
		else:
			raise exceptions.UnknownPred(pred, self)

		pred_idx = self.pred_to_vm_index[pred]
		offset   = self.offset[pred_idx]

		# to_return  = offset
		# multiplier = 1
		# for slot, dep in zip(value_slots, deps):
		# 	to_return  += slot * multiplier
		# 	multiplier *= dep
		print(value_slots, deps)
		return offset + np.ravel_multi_index(value_slots, deps, order = "F")


def grand_product(list_numbers):
	"""
	Computes grand product of a list.
	[1, 2, 3] -> 6 (= 2 * 3)
	"""
	to_return = 1
	for nb in list_numbers:
		to_return *= nb
	return to_return
	




