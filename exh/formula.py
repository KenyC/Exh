import numpy as np
from collections import defaultdict
import itertools

from IPython.display import Math, display, HTML

import exh.formula_simplify
import exh.formula_display
import exh.formula_evaluate

import exh.utils as utils
import exh.options as options
from exh.vars import VarManager


@utils.add_functions_as_methods(exh.formula_simplify.methods + exh.formula_display.methods + exh.formula_evaluate.methods)
class Formula:

	def __init__(self, typeF, *child):
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

	def __eq__(self, other):
		if self.type == other.type:
			if self.type == "var" or self.type == "neg":
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
	def flatten(self):
		if self.type in ["and", "or"]:
			new_children = list(self.iterator_type())
		else:
			new_children = self.children

		return Formula(self.type, *map(lambda c: c.flatten(), new_children))
	

	"""
	Turns a formula into a quantifier-first, disjunctions of conjunctions formula
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


	def vars(self):
		self.vm = VarManager.merge(*[c.vars() for c in self.children])
		self.vm.linearize()
		return self.vm



# def Var(number):
# 	return Formula("var", number)














############### VARIABLE CLASS ################


class Var(Formula):

	def __init__(self, number, depends_on = None, name = None):
		self.deps = depends_on if depends_on is not None else set()
		self.name = name
		super(Var, self).__init__("var", number)


	def flatten(self):
		return self

	def simplify(self):
		return self

	def display_aux(self, display_dict):
		if self.deps:
			dep_string = "({})".format(",".join(list(self.deps)))
		else:
			dep_string = ""
		
		if self.name is None:
			return "A{}".format(self.children[0]) + dep_string
		else:
			return self.name + dep_string


	def evaluate_aux(self, assignment, vm, variables = dict()):
		return assignment[:, vm.index(self.idx, **variables)]



	def depends_on(self, var):
		self.deps.add(var)

	def __call__(self, *variables):
		for var in variables:
			self.depends_on(var)

		return self

	def vars(self):

		if self.name is None:
			self.vm = VarManager({self.idx: self.deps})
		else:
			self.vm = VarManager({self.idx: self.deps}, names = {self.name: self.idx})

		return self.vm

	@property
	def idx(self):
		return self.children[0]

	


a = Var(0, name = "a")
b = Var(1, name = "b")
c = Var(2, name = "c")

f1 = a & b & ~c
f2 = a | b & c

