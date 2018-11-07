from assignment import getAssignment
import numpy as np

class Universe:

	def __init__(self, n, worlds = None):
		
		self.n = n

		if worlds is None:
			self.worlds = getAssignment(n)
		else:
			self.worlds = worlds

	def consistent(self, *fs):
		output = np.full(len(self.worlds), True, dtype = "bool")

		for f in fs:
			output = np.logical_and(output, f.evaluate(self.worlds))

		return np.any(output)

	def evaluate(self, *fs):
		return np.transpose(np.stack([f.evaluate(self.worlds) for f in fs]))

	def restrict(self, indices):
		return Universe(self.n, self.worlds[indices])