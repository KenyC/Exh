from assignment import getAssignment
from vars import VarManager
import numpy as np

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
		output = np.full(len(self.worlds), True, dtype = "bool")

		for f in fs:
			output = np.logical_and(output, f.evaluate(self.worlds))

		return np.any(output)


	def evaluate(self, *fs):
		return np.transpose(np.stack([f.evaluate(self.worlds, vm = self.vm) for f in fs]))

	def restrict(self, indices):
		return Universe(vm = self.vm, worlds = self.worlds[indices])