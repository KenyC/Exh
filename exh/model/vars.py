from . import options
from . import exceptions

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
		preds             -- a dictionary mapping predicate names to the variables they depend on
		pred_to_vm_index  -- a dictionary mapping predicate names to their position in preds
		names             -- a dictionary mapping predicate names to their indices
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

		self.memory = [options.dom_quant ** ndeps  for _, ndeps in self.preds.items()]
		
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
		offset = self.offset[pred_idx]
		
		return offset + sum(slot * (options.dom_quant ** i)  for i, slot in enumerate(value_slots))
	




