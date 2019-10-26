from formula import *


class Quantifier(Formula):
	def __init__(self, quant_var, scope):
		super(Quantifier, self).__init__("quant", scope)
		self.symbol = "Q"
		self.qvar = quant_var

	def display():
		return "{symb} {var}, {scope}".format(symb = self.symbol, var = VAR_NAMES[self.qvar], scope = self.children[0].display()) 

	def evaluate_aux(self, assignment, variables, vm):
		return self.fun([self.children[0].evaluate_aux(assignment, variables., vm) for i in range(options.dom_quant)])

	def fun(self, results):
		raise Exception("Evaluation of abstract class Quantifier ; use Universal or Existential class")



class Universal(Quantifier):

	def __init__(self, *args, **kwargs):
		super(Universal, self).__init__(*args, **kwargs)
		self.symbol = "\u2200"

class Existential(Quantifier):

	def __init__(self, *args, **kwargs):
		super(Existential, self).__init__(*args, **kwargs)
		self.symbol = "\u2203"