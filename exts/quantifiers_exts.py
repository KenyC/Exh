import numpy as np

import exh.quantifier as q


class Most(q.Quantifier):

	def __init__(self, *args, **kwargs):
		super(Most, self).__init__(*args, **kwargs)
		self.symbol = "Most"
		self.type = "most"

	def fun(self, results):
		return np.mean(results, axis = 0) > 0.5

	def display_aux(self, display_dict):
		return "\\text{{Most }} {var}, {scope}".format(var = self.qvar,
											 scope = self.children[0].display_aux(display_dict))



class NumeralQuantifier(q.Quantifier):

	def fun(self, results):
		return self.numerosity(np.sum(results, axis = 0))

	def numerosity(self, counts):
		raise Exception("Abstract class NumeralQuantifier can't be instantiated")


class ExactlyNQuantifier(NumeralQuantifier):

	def __init__(self, n, *args, **kwargs):
		self.n = n
		super(ExactlyN, self).__init__(*args, **kwargs)
		self.plain_symbol = self.latex_symbol = str(self.n)

	def numerosity(self, counts):
		return counts == self.n


M = q.quantifier_cons(Most)

Mx = M("x")
My = M("y") 
Mz = M("z")

def ExactlyN(n, var):
	return q.C(lambda formula: ExactlyNQuantifier(n, var, formula))