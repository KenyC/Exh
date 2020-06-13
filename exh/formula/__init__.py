import numpy as np
from collections import defaultdict
import itertools

from IPython.display import Math, display, HTML

from .simplify import methods as f_simplify
from .display import methods as f_display
from .evaluate import methods as f_evaluate

from .. import utils
from .. import options
from ..vars import VarManager


@utils.add_functions_as_methods(f_simplify + f_display + f_evaluate)
class Formula:

	# LateX display for the different formulas
	latex_dict = {"and": r"\wedge", "or": r"\vee", "not": r"\neg",
				 "exh": r"Exh"}

	# Plain text display for the different formulas
	plain_dict = {"and": "and", "or": "or", "not": "not",
				 "exh": r"Exh"}

	substitutable = True

	def __init__(self, typeF, *child):
		self.subst = self.__class__.substitutable
		self.children = child
		self.type = typeF
		self.vars()

	def __and__(self, other):
		return Formula("and", self, other)

	def __or__(self, other):
		return Formula("or", self, other)

	def __invert__(self):
		return Formula("not", self)

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
		if self.type == other.type:
			if self.type == "pred" or self.type == "neg":
				return self.children[0] == other.children[0]

			elif self.type == "or" or self.type == "and":

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
		self.vm = VarManager.merge(*[c.vars() for c in self.children])
		self.vm.linearize()
		return self.vm





############### VARIABLE CLASS ################

"""
Class for atomic proposition and predicate variable

Attributes:
	- name : name for display and evaluation
	- deps : for n-ary predicates, the set of variables that the predicate depends on
	- idx : an integer that uniquely identifies the predicate
"""
def automatic_var_names():
	typical_names = ["x{}", "y{}", "z{}"]

	for x in itertools.chain([""], itertools.count()):
		for var in typical_names:
			yield var.format(x)

class Pred(Formula):


	def __init__(self, index, name = None, arity = 0, depends_on = None):
		self.name = name
		self.set_arity(arity, depends_on)

		super(Pred, self).__init__("pred", index)


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


	def evaluate_aux(self, assignment, vm, variables = dict()):
		value_slots = [variables[dep] for dep in self.deps]
		return assignment[:, vm.index(self.idx, value_slots)]


	def __call__(self, *variables):
		if len(variables) == self.arity:
			return Pred(self.idx, self.name, self.arity, variables)
		elif len(variables) > self.arity:
			raise Exception("More variables were provided than the predicate {} depends on".format(self.name))
		else:
			raise Exception("Less variables were provided than the predicate {} depends on".format(self.name))

	def vars(self):

		if self.name is None:
			self.vm = VarManager({self.idx: self.arity})
		else:
			self.vm = VarManager({self.idx: self.arity}, names = {self.name: self.idx})

		return self.vm

	@property
	def idx(self):
		return self.children[0]






	def set_arity(self, n, depends_on = None):
		self.arity = arity

		if depends_on is None: # automatic variable naming
			self.deps = [var_name for _, var_name in zip(range(self.arity), automatic_var_names())]
		elif len(depends_on) == self.arity:
			self.deps = depends_on
		elif len(depends_on) > self.arity:
			raise Exception("More variables are named than the predicate depends on")
		else:
			raise Exception("Less variables are named than the predicate depends on")
	


a = Pred(0, name = "a")
b = Pred(1, name = "b")
c = Pred(2, name = "c")

f1 = a & b & ~c
f2 = a | b & c

