from assignment import getAssignment
from prettytable.prettytable import PrettyTable, PLAIN_COLUMNS
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

	def truthTable(self, *fs):
		output = self.evaluate(*fs)

		t = PrettyTable()
		t.field_names = [" A"+str(i) +" " for i in range(self.n)] + [str(f) for f in fs]
		# t.set_style(PLAIN_COLUMNS)

		for i in range(len(output)):
			t.add_row(list(self.worlds[i].astype("int"))+list(output[i].astype("int")))

		print(t)

	def equivalent(self,f,g):
		return self.evaluate(f) == self.evaluate(g)

	def consistent(self, *l):
		return np.amax(np.amin(self.evaluate(*l), axis = 1), axis = 0)

	def restrict(self, indices):
		return Universe(self.n, self.worlds[indices])