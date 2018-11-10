import numpy as np
from formula import Formula
import options

class E(Formula):

	def __init__(self, child, sizeDomain = options.qDomain):
		self.sizeDomain = sizeDomain
		super(E, self).__init__("some",child)

	def display(self):
		return "E[{}]".format(self.children[0].display())

	def eq(self, other):
		return (other.type == "some") and (other.children[0] == self.children[0])

	def vars(self):
		return [self.sizeDomain*var + i for var in self.children[0].vars() for i in range(self.sizeDomain)]

	def evaluate(self, assignment):

		subContextEval = np.concatenate([assignment[:,i::self.sizeDomain] for i in range(self.sizeDomain)])
		
		return np.amax(np.transpose(np.stack(np.split(self.children[0].evaluate(subContextEval), self.sizeDomain))), axis = 1)


def U(Formula):

	def __init__(self, child, sizeDomain = options.qDomain):
		self.sizeDomain = sizeDomain
		super(U, self).__init__("all",child)

	def display(self):
		return "U[{}]".format(self.children[0].display())

	def eq(self, other):
		return (other.type == "all") and (other.children[0] == self.children[0])

	def vars(self):
		return [self.sizeDomain*var + i for var in self.children[0].vars() for i in range(self.sizeDomain)]

	def evaluate(self, assignment):

		subContextEval = np.concatenate([assignment[:,i::self.sizeDomain] for i in range(self.sizeDomain)])
		
		return np.amin(np.transpose(np.stack(np.split(self.children[0].evaluate(subContextEval), self.sizeDomain))), axis = 1)

		

