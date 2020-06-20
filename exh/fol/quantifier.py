import numpy as np
from collections import defaultdict

import exh.model.options as options
import exh.prop as prop

class Quantifier(prop.Formula):
	"""
	Abstract class for quantified formula

	Attributes:
		symbol -- display symbol (obsolete)
		qvar   -- string name of the individual variable of quantification
	"""

	substitutable = False
	plain_symbol = "Q"
	latex_symbol = "Q"

	def __init__(self, quant_var, scope):
		super(Quantifier, self).__init__(scope)
		self.qvar = quant_var

		try:
			self.free_vars.remove(self.qvar)
		except ValueError:
			pass

	def display_aux(self, latex):
		return "{symb} {var}, {scope}".format(symb = self.__class__.latex_symbol if latex else self.__class__.plain_symbol,
											 var   = self.qvar,
											 scope = self.children[0].display_aux(latex)) 

	def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):
		return self.fun(np.stack([self.children[0].evaluate_aux(assignment, vm, 
		                                                        dict(variables, **{self.qvar: i}),
		                                                        free_vars) 
		                         for i in range(options.dom_quant)],
		                         axis = 0))

	def fun(self, results):
		raise Exception("Evaluation of abstract class Quantifier ; use Universal or Existential class")

	def __eq__(self, other):
		if self.type == other.type:
			if self.qvar == other.qvar:
				return self.children[0] == other.children[0]
		return False

	@property
	def scope(self):
		return self.children[0]
	

	def copy(self):
		return self.__class__(self.qvar, self.scope)


class Universal(Quantifier):
	plain_symbol = "\u2200"
	latex_symbol = r"\forall"

	def __init__(self, *args, **kwargs):
		super(Universal, self).__init__(*args, **kwargs)
		self.type = "all"

	def fun(self, results):
		return np.min(results, axis = 0)

class Existential(Quantifier):
	plain_symbol = "\u2203"
	latex_symbol = r"\exists"

	def __init__(self, *args, **kwargs):
		super(Existential, self).__init__(*args, **kwargs)
		self.type = "some"

	def fun(self, results):
		return np.max(results, axis = 0)

class C:
	"""
	The following baroque construction allows us to write quantifierd formula in parenthesis-free way:
	Ax > Ey > a | b
	To do this, we twist Python in ways that are not recommendable for other purposes.
	Reasonable usage of the library should not incur any problems.

	The class C is such that "C() > formula37" will return a formula built from "formula37" using function cons
	"""

	def __init__(self, function):
		self.cons = function
		self.bup = function

	def __gt__(self, other): 
		"""
		In python, A > B > C is evaluated as (A > B) and (B > C) ; 
		this is not the semantics we want so we allow A>B to change the value of B before evaluation in conjunct (B>C)
		This is highly unorthodox ; don't try this at home
		"""
		return_val = True
		if isinstance(other, prop.Formula):
			return_val = self.cons(other)
		else:
			f = other.cons # We store a reference to the original function so that the lambda term is not interpreted recursively
			other.cons = lambda formula: self.cons(f(formula))

		self.cons = self.bup # We restore the original function in case chaining has happened
		return return_val

		

def quantifier_cons(constructor):
	""" Returns a C class from a formula constructor """
	def f(var):
		return C(lambda formula: constructor(var, formula))

	return f


