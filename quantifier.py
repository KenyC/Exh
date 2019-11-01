from formula import *
from collections import defaultdict

class Quantifier(Formula):
	def __init__(self, quant_var, scope):
		super(Quantifier, self).__init__("quant", scope)
		self.symbol = "Q"
		self.qvar = quant_var

	def display(self):
		return "{symb}{var}, {scope}".format(symb = self.symbol, var = self.qvar, scope = self.children[0].display()) 

	def evaluate_aux(self, assignment, variables = dict(), vm = None):
		if vm is None:
			vm = self.vars()

		return self.fun(np.stack([self.children[0].evaluate_aux(assignment, dict(variables, **{self.qvar: i}), vm) for i in range(options.dom_quant)], axis = 0))

	def fun(self, results):
		raise Exception("Evaluation of abstract class Quantifier ; use Universal or Existential class")



class Universal(Quantifier):

	def __init__(self, *args, **kwargs):
		super(Universal, self).__init__(*args, **kwargs)
		self.symbol = "\u2200"
		self.type = "all"

	def fun(self, results):
		return np.min(results, axis = 0)

class Existential(Quantifier):

	def __init__(self, *args, **kwargs):
		super(Existential, self).__init__(*args, **kwargs)
		self.symbol = "\u2203"
		self.type = "some"

	def fun(self, results):
		return np.max(results, axis = 0)

# The followin baroque construction allows us to write quantifierd formula in parenthesis-free way:
# Ax > Ey > a | b
# To do this, we twist Python in ways that are not recommendable for other purposes
# Reasonable usage of the library should not incur any problems
class C:
	def __init__(self, function):
		self.cons = function
		self.bup = function

	def __gt__(self, other): 
		# In python, A > B > C is evaluated as (A > B) and (B > C) ; 
		# this is not the semantics we want so we allow A>B to change the value of B before evaluation in conjunct 2
		# This is highly unorthodox ; don't try at home
		return_val = True
		if isinstance(other, Formula):
			return_val = self.cons(other)
		else:
			f = other.cons # We store a reference to the original function so that the lambda term is not interpreted recursively
			other.cons = lambda formula: self.cons(f(formula))

		self.cons = self.bup # We restore the original function in case chaining has happened
		return return_val


def quantifier_cons(constructor):
	def f(var):
		return C(lambda formula: constructor(var, formula))

	return f

U = quantifier_cons(Universal)
E = quantifier_cons(Existential)

Ax = U("x")
Ex = E("x")

Ay = U("y")
Ey = E("y")

Az = U("z")
Ez = E("z")
