import exh.options as options
import exh.exceptions as exceptions

"""
VarManager keeps track of all independent variables in a given system.
Maps propositional variables and fully saturated predicate variables to indices

Example: 
System: unary predicate p and proposition q; domain of individuals = 3
Values: p(0) p(1) p(2) q
are mapped to
Indices: 0    1    2   3
"""
class VarManager:

	def __init__(self, preds, names = dict()):
		self.preds = preds
		self.names = names

		self.var_to_vm_index = {var_idx: vm_idx for vm_idx, var_idx in enumerate(self.preds.keys())}
		self.linearize()

	def linearize(self):
		# All individual variables recorded
		self.dependencies = set(dep for value in self.preds.values() for dep in value)
		self.pred_index = list(self.preds.keys())

		# How many independent boolean values to specify the propositional variables.
		# propositions: 1 i
		# unary predicate: dom_quant
		# etc
		self.memory = [options.dom_quant ** len(deps)  for pred, deps in self.preds.items()]
		
		self.offset = [0]
		for mem in self.memory[:-1]:
			self.offset.append(self.offset[-1] + mem)

	def merge(*vms):
		return VarManager(preds = {k: v for vm in vms for k, v in vm.preds.items()},
						  names = {k: v for vm in vms for k, v in vm.names.items()})

	@property
	def n(self):
		return sum(self.memory)

	def index(self, pred, **variables):
		if pred in self.preds:
			deps = self.preds[pred]
		else:
			raise exceptions.UnknownPred(pred, self)

		pred_idx = [i for i, key in enumerate(self.preds.keys()) if key == pred][0]
		offset = self.offset[pred_idx]
		
		return offset + sum(variables[dep] * (options.dom_quant ** i)  for i, dep in enumerate(deps) if dep in variables)
	




