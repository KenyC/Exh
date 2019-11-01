import options

class VarManager:

	def __init__(self, preds):
		self.preds = preds
		self.linearize()

	def linearize(self):
		self.dependencies = set(dep for value in self.preds.values() for dep in value)
		self.pred_index = list(self.preds.keys())
		self.memory = [options.dom_quant ** len(deps)  for pred, deps in self.preds.items()]
		
		self.offset = [0]
		for mem in self.memory[:-1]:
			self.offset.append(self.offset[-1] + mem)

	def merge(*vms):
		return VarManager(preds = {k: v for vm in vms for k, v in vm.preds.items()})

	@property
	def n(self):
		return sum(self.memory)
	




