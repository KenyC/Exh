import numpy as np

import exh.model          as var
import exh.utils          as utils
import exh.model.options  as options

from exh.prop.formula import Formula


############### PREDICATE CLASS ################

class Focus(Formula):
	"""
	Class for focused item
		- child : formula corresponding to focused element
		- alts  : alternatives
	"""

	no_parenthesis = True
	substitutable  = False

	def __init__(self, child, alts):
		self.alts = alts
		super(Focus, self).__init__(child)



	# @profile
	def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):
		# Not necessary to split by "free_vars", the empty case is just a special case
		# The split avoids generalizing to the worst case.
		return self.children[0].evaluate_aux(assignment, vm, variables, free_vars)






	def __eq__(self, other):
		return super(Focus, self).__eq__(other) and self.children[0] == other.children[0]


	def display_aux(self, latex):
		child = self.children[0]
		formula = (
			"{}" if child.no_parenthesis
			else "({})"
		).format(child.display_aux(latex)) 


		if latex:
			return "{}_{{F}}".format(formula)
		else:
			return "{}_F".format(formula)

	def vars(self):
		"""Returns a VariableManager object for all the variables that occur in the formula"""

		self.vm = var.VarManager.merge(self.children[0].vars(), *(alt.vars() for alt in self.alts))
		self.vm.linearize()
		return self.vm