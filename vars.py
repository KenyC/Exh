import options

class VarManager:

	def __init__(self, preds, names = dict()):
		self.preds = preds
		self.names = names
		self.linearize()

	def linearize(self):
		self.dependencies = set(dep for value in self.preds.values() for dep in value)
		self.pred_index = list(self.preds.keys())
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
		deps = self.preds[pred]

		pred_idx = [i for i, key in enumerate(self.preds.keys()) if key == pred][0]
		offset = self.offset[pred_idx]
		
		return offset + sum(variables[dep] * (options.dom_quant ** i)  for i, dep in enumerate(deps) if dep in variables)
	




