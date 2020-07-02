import numpy as np
from collections import defaultdict
import itertools

from IPython.display import Math, display, HTML

import exh.utils         as utils
import exh.model.options as options
import exh.model.vars    as var

from .simplify import IteratorType
from .display  import Display
from .evaluate import Evaluate


class Formula(IteratorType, Display, Evaluate): # Using sub-classing to spread code over multiple files
	"""
	Base class for fomulas

	Class attributes:
		no_parenthesis (bool) -- whether to display the formula with parenthesis around it in conjunctions, coordinations, etc.
		substitutable  (bool) -- Whether sub-formulas of this formulas count as alternatives to it

	Attributes:
		children (list(Formula)) -- sub-formulas
		vm (VariableManager)     -- organizes mapping from predicate and variables name to concrete bit position
	"""

	no_parenthesis = False
	substitutable = True

	def __init__(self, *children):
		self.subst = self.__class__.substitutable
		self.children = children
		self.vars()

		# Free vars are lexically ordered
		self.free_vars = list(set(var for child in self.children for var in child.free_vars)) 
		self.free_vars.sort()

	def reinitialize(self): #only used for Exh, which performs computation at initialization
		pass

	def __and__(self, other):
		return And(self, other)

	def __or__(self, other):
		return Or(self, other)

	def __invert__(self):
		return Not(self)

	def __str__(self):
		return self.display()

	def __repr__(self):
		return self.display()

	def copy(self):
		"""Creates copy of the object (overridden by children's classes"""
		return Formula(*self.children)

	def __eq__(self, other):
		"""Returns true if two formulas are syntactically the same, up to constituent reordering (overridden by children classes)"""
		return self.__class__ is other.__class__


	
	### FORMULA MANIPULATION METHODS ###
	def flatten(self):
		"""
		Turns embedded "or" and "and" in to generalized "or" and "and"
		Ex: a or ((b or c) or d) becomes a or b or c or d 
		"""
		raise Exception("Not implemented yet!")

		if self.type in ["and", "or"]:
			new_children = list(self.iterator_type())
		else:
			new_children = self.children

		return Formula(self.type, *map(lambda c: c.flatten(), new_children))
	

	def simplify(self):
		"""Turns a formula into a quantifier-first, disjunctions of conjunctions formula"""
		raise Exception("Not implemented yet!")

		# Returns all indexes of variables in a conjunctive formula
		def idx_vars(f):
			return [child.idx if "idx" in dir(child) else -1 for child in f.iterator_type("and")]

		if self.type == "or" or self.type == "and":
			simplified_children = [child.simplify() for child in self.iterator_type()]

			if self.type == "or":
				all_children = [grandchild for child in simplified_children for grandchild in child.iterator_type("or")]
				all_children.sort(key = idx_vars)

				return Formula("or", *all_children)

			else:
				all_children = [list(child.iterator_type("or")) for child in simplified_children]
				individual_conjuncts = TODO

				return self
		elif self.type == "neg":
			child = self.children[0]

			if child.type == "or":
				pass
		else:
			return self

	def vars(self):
		"""Returns a VariableManager object for all the variables that occur in the formula"""

		self.vm = var.VarManager.merge(*[c.vars() for c in self.children])
		self.vm.linearize()
		return self.vm



############### OPERATORS ##############

class Operator(Formula):
	"""
	Base class for associative operators

	Class attributes:
		plain_symbol (str) -- symbol to display in plain text mode (to be overridden by children classes)
		latex_symbol (str) -- symbol to display in LateX mode (to be overridden by children classes)

	Attributes:
		fun (function) -- function to call on subformulas' result to get parent result
	"""


	plain_symbol = "op"
	latex_symbol = "\text{op}"

	def __init__(self, fun, *children):
		super(Operator, self).__init__(*children)
		self.fun = fun
						
	def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):
		"""Stacks subformulas' results and applies fun to it"""
		return self.fun(np.stack([child.evaluate_aux(assignment, vm, variables, free_vars) for child in self.children]))


	def display_aux(self, latex):

		if latex:
			symbol = self.__class__.latex_symbol
		else:
			symbol = self.__class__.plain_symbol

		def paren(child):
			if (self.__class__ is child.__class__) or child.__class__.no_parenthesis:
				return child.display_aux(latex)
			else:
				return "({})".format(child.display_aux(latex))

		if len(self.children) == 1:
			return "{}[{}]".format(symbol, self.children[0].display_aux(latex))
		else:
			return " {type} ".format(type = symbol).join([paren(child) for child in self.children])

	def __eq__(self, other):
		if self.__class__ is other.__class__:
			other_children = list(other.children)
			
			for child1 in self.children:
					
				matches = [i for i, child2 in enumerate(other_children) if child1 == child2]

				if matches:
					other_children.pop(matches[0])
				else:
					return False

			return True
		else:
			return False


class And(Operator):
	plain_symbol = "and"
	latex_symbol = r"\land"

	fun_ = lambda array: np.min(array, axis = 0)

	"""docstring for And"""
	def __init__(self, *children):
		super(And, self).__init__(And.fun_, *children)
		

class Or(Operator):
	plain_symbol = "or"
	latex_symbol = r"\lor"
	
	fun_ = lambda array: np.max(array, axis = 0)

	"""docstring for Or"""
	def __init__(self, *children):
		super(Or, self).__init__(Or.fun_, *children)
		
class Not(Operator):
	no_parenthesis = True

	plain_symbol = "not"
	latex_symbol = r"\neg"

	fun_ = lambda x: np.squeeze(np.logical_not(x), axis = 0)

	"""docstring for Not"""
	def __init__(self, child):
		super(Not, self).__init__(Not.fun_, child)




############### TAUTOLOGIES AND ANTILOGIES ########

class Truth(Formula):
	"""docstring for Truth"""
	def __init__(self):
		super(Truth, self).__init__()

	def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):
		return np.ones(assignment.shape[0], dtype = "bool")

	def display_aux(self, latex):
		if latex:
			return r"\textsf{true}"
		else:
			return "true"


class Falsity(Formula):
	"""docstring for Falsity"""
	def __init__(self):
		super(Falsity, self).__init__()

	def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):
		return np.zeros(assignment.shape[0], dtype = "bool")

	def display_aux(self, latex):
		if latex:
			return r"\textsf{true}"
		else:
			return "true"


