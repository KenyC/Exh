import options

class VarManager:

	def __init__(self, preds):
		self.preds = {pred: [] for pred in props}

	def linearize(self):
		self.dependencies = set(dep for value in self.preds.values() for dep in value)
		self.pred_index = list(self.preds.keys())
		self.memory = [options.dom_quant ** len(deps)  for pred, deps in self.preds.dict_items()]
		
		self.offset = [self.memory[0]]
		for mem in self.memory[1:]:
			self.offset.append(self.offset[-1] + mem)




