"""
A module for a variety of Generalized Quantifiers and associated scales, including

	- most/more than half
	- modified numerals
"""

import numpy as np
import exh.fol as q



class Most(q.Quantifier):
	plain_symbol = "Most "
	latex_symbol = "\\text{Most }"

	def __init__(self, *args, **kwargs):
		super(Most, self).__init__(*args, **kwargs)
		self.symbol = "Most"
		self.type   = "most"

	def fun(self, results):
		return np.mean(results, axis = 0) > 0.5




class NumeralQuantifier(q.Quantifier):

	def fun(self, results):
		return self.numerosity(np.sum(results, axis = 0))

	def numerosity(self, counts):
		raise Exception("Abstract class NumeralQuantifier can't be instantiated")


class ExactlyQuantifier(NumeralQuantifier):
	plain_symbol = "Exactly "
	latex_symbol = "\\text{{Exactly }}"

	def __init__(self, n, *args, **kwargs):
		self.n = n
		super(ExactlyQuantifier, self).__init__(*args, **kwargs)

		self.plain_symbol += str(self.n)
		self.latex_symbol += str(self.n)

	def numerosity(self, counts):
		return counts == self.n


class MoreThanQuantifier(NumeralQuantifier):
	plain_symbol = "More than "
	latex_symbol = "\\text{{More than }}"

	def __init__(self, n, *args, **kwargs):
		self.n = n
		super(MoreThanQuantifier, self).__init__(*args, **kwargs)

		self.plain_symbol += str(self.n)
		self.latex_symbol += str(self.n)

	def numerosity(self, counts):
		return counts > self.n

class LessThanQuantifier(NumeralQuantifier):
	plain_symbol = "Less than "
	latex_symbol = "\\text{{Less than }}"

	def __init__(self, n, *args, **kwargs):
		self.n = n
		super(LessThanQuantifier, self).__init__(*args, **kwargs)

		self.plain_symbol += str(self.n)
		self.latex_symbol += str(self.n)

	def numerosity(self, counts):
		return counts < self.n


M = q.quantifier_cons(Most)

Mx = M("x")
My = M("y") 
Mz = M("z")

def Exactly(n, var):
	return q.C(lambda formula: ExactlyQuantifier(n, var, formula))

def LessThan(n, var):
	return q.C(lambda formula: LessThanQuantifier(n, var, formula))

def MoreThan(n, var):
	return q.C(lambda formula: MoreThanQuantifier(n, var, formula))