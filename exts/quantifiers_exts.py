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

M = q.quantifier_cons(Most)

Mx = M("x")
My = M("y") 
Mz = M("z")
