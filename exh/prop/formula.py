import numpy as np
from collections import defaultdict
import itertools

from IPython.display import Math, display, HTML

from .simplify import IteratorType
from .display  import Display
from .evaluate import Evaluate

import exh.utils         as utils
import exh.model.options as options
import exh.model.vars    as var



class Formula(IteratorType, Display, Evaluate): # Use sub-classing to spread code over multiple files
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
		return Formula(self.type, *self.children)

	"""
	Returns true if two formulas are syntactically the same, up to constituent reordering
	"""
	def __eq__(self, other):
		return self.__class__ is other.__class__


	
	### FORMULA MANIPULATION METHODS ###
	"""
	Turns embedded "or" and "and" in to generalized "or" and "and"
	Ex: a or ((b or c) or d) becomes a or b or c or d 
	"""
	def flatten(self):
		if self.type in ["and", "or"]:
			new_children = list(self.iterator_type())
		else:
			new_children = self.children

		return Formula(self.type, *map(lambda c: c.flatten(), new_children))
	

	"""
	Turns a formula into a quantifier-first, disjunctions of conjunctions formula
	TODO
	"""
	def simplify(self):
		raise NotImplementedError

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

	"""
	Returns a VariableManager object for all the variables that occur in the formula
	"""
	def vars(self):
		self.vm = var.VarManager.merge(*[c.vars() for c in self.children])
		self.vm.linearize()
		return self.vm



############### OPERATORS ##############

class Operator(Formula):
	plain_symbol = "op"
	latex_symbol = "\text{op}"

	"""docstring for Operator"""
	def __init__(self, fun, *children):
		super(Operator, self).__init__(*children)
		self.fun = fun
						
	def evaluate_aux(self, assignment, vm, variables = dict()):
		return self.fun(np.stack([child.evaluate_aux(assignment, vm, variables) for child in self.children]))


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

	"""docstring for And"""
	def __init__(self, *children):
		super(And, self).__init__(lambda array: np.min(array, axis = 0), *children)
		

class Or(Operator):
	plain_symbol = "or"
	latex_symbol = r"\lor"
	
	"""docstring for Or"""
	def __init__(self, *children):
		super(Or, self).__init__(lambda array: np.max(array, axis = 0), *children)
		
class Not(Operator):
	no_parenthesis = True

	plain_symbol = "not"
	latex_symbol = r"\neg"

	"""docstring for Not"""
	def __init__(self, child):
		super(Not, self).__init__(lambda x: np.squeeze(np.logical_not(x), axis = 0), child)




############### TAUTOLOGIES AND ANTILOGIES ########

class Truth(Formula):
	"""docstring for Truth"""
	def __init__(self):
		super(Truth, self).__init__()

	def evaluate_aux(self, assignment, vm, variables = dict()):
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

	def evaluate_aux(self, assignment, vm, variables = dict()):
		return np.zeros(assignment.shape[0], dtype = "bool")

	def display_aux(self, latex):
		if latex:
			return r"\textsf{true}"
		else:
			return "true"


true  = Truth()
false = Falsity()


############### PREDICATE CLASS ################

"""
Class for atomic proposition and predicate variable
Attributes:
	- name : name for display and evaluation
	- arity : for n-ary predicates, the number of variables that the predicate depends on
	- deps : the name of the default variables that the predicate depends 
	(i.e. when no vars are specified, as in Ax > a, this is what the predicate depends on)
	- idx : an integer that uniquely identifies the predicate
"""
class Pred(Formula):
	no_parenthesis = True


	def __init__(self, index, name = None, depends = None):
		self.name = name

		if depends is None:
			depends = []
		elif isinstance(depends, str):
			depends = [depends]
		elif isinstance(depends, int):
			depends = [depends]

		self.depends(*depends)

		self.idx = index
		super(Pred, self).__init__()

		self.free_vars = list(set(self.deps))
		self.free_vars.sort()


	def flatten(self):
		return self

	def simplify(self):
		return self

	def display_aux(self, latex):
		if self.deps:
			dep_string = "({})".format(",".join(list(self.deps)))
		else:
			dep_string = ""
		
		if self.name is None:
			return "A{}".format(self.children[0]) + dep_string
		else:
			return self.name + dep_string


	def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):
		# Not necessary to split by "free_vars", the empty case is just a speical case
		# The split avoids generalizing to the worst case.
		if not free_vars: 
			value_slots = [variables[dep] for dep in self.deps]
			return assignment[:, vm.index(self.idx, value_slots)]
		else:
			shape_output           = tuple(options.dom_quant for _ in free_vars)
			vars_not_in_assignment = set(self.deps).difference(set(variables.keys()))

			position_free_vars = np.full(len(free_vars), True)
			for dep in vars_not_in_assignment: 
				position_free_vars[free_vars.find(dep)] = False #Potential for exception if free_vars is misconfigured

			value_slots    = np.full(len(self.deps), 0,     dtype = "int") 
			mask_free_vars = np.full(len(self.deps), False, dtype = "bool") 

			for i, dep in enumerate(self.deps):
				if dep in variables:
					value_slots[i]    = variables[dep]
				else:
					mask_free_vars[i] = True

			output = np.full((len(assignment), *shape_output), True, dtype = "bool")
			grid   = np.indices(shape_output) 

			for index in np.ndindex(shape_output):
				value_slots[mask_free_vars] = np.array(index)[position_free_vars]
				output[:, *index] = assignment[:, vm.index(self.idx, value_slots)]

			return output






	def __call__(self, *variables):
		if len(variables) == self.arity:
			return Pred(self.idx, self.name, variables)
		else:
			print("""WARNING: {} variables were provided than the predicate {} depends on ; changing the arity of the predicate to {}. Universe objects will need to be recreated."""
			      .format("More" if len(variables) > self.arity else "Less", self.name, len(variables)))
			self.depends(*variables)
			return self

	def __eq__(self, other):
		return super(Pred, self).__eq__(other) and self.idx == other.idx

	def vars(self):

		if self.name is None:
			self.vm = var.VarManager({self.idx: self.arity})
		else:
			self.vm = var.VarManager({self.idx: self.arity}, names = {self.name: self.idx})

		return self.vm




	def depends(self, *depends_on):
		if depends_on and isinstance(depends_on[0], int):
			self.arity = depends_on[0]
			self.deps = [var_name for _, var_name in zip(range(self.arity), utils.automatic_var_names())]
		else:
			self.arity = len(depends_on)
			self.deps = depends_on




a = Pred(0, name = "a")
b = Pred(1, name = "b")
c = Pred(2, name = "c")


if __name__ == "__main__":
	f1 = a & b & ~c
	f2 = a | b & c

