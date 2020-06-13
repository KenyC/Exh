class UnknownPred(Exception):
	def __init__(self, var, vm):
		self.var = var
		self.vm = vm
		super(UnknownPred, self).__init__("Unknown predicate with index {pred}. Known indices: {vmvars}".format(pred = var,
																									vmvars = list(vm.names.keys())))

