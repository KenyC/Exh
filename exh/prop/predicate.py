import numpy as np

import exh.model.vars     as var
import exh.utils          as utils
import exh.model.options  as options

from .formula import Formula


############### PREDICATE CLASS ################

class Pred(Formula):
	"""
	Class for atomic proposition and predicate variable
	Attributes:
		- name : name for display and evaluation
		- arity : for n-ary predicates, the number of variables that the predicate depends on
		- deps : the name of the default variables that the predicate depends 
		(i.e. when no vars are specified, as in Ax > a, this is what the predicate depends on)
		- idx : an integer that uniquely identifies the predicate
	"""

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

		self.free_vars = self.free_vars_

	@property
	def free_vars_(self):
		return sorted(set(self.deps))
	

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

	# @profile
	def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):
		# Not necessary to split by "free_vars", the empty case is just a special case
		# The split avoids generalizing to the worst case.
		if not free_vars: 
			try:
				value_slots = [variables[dep] for dep in self.deps]
			except KeyError as e:
				raise Exception("Predicate {} cannot be evaluated b/c no value for free variable {} was provided".format(self.name, e))

			return assignment[:, vm.index(self.idx, value_slots)]
		else:
			""" 
			P(x, y, z)
			The value of some of these variables are provided by assignment, others are left free
			"""
			shape_output           = tuple(options.dom_quant for _ in free_vars)
			vars_not_in_assignment = set(self.deps).difference(set(variables.keys()))

			position_free_vars = np.full(len(free_vars), False)
			for dep in vars_not_in_assignment: 
				position_free_vars[free_vars.index(dep)] = True #Potential for exception if free_vars is misconfigured

			value_slots    = np.full(len(self.deps), 0,     dtype = "int") 
			mask_free_vars = np.full(len(self.deps), False, dtype = "bool") 

			for i, dep in enumerate(self.deps):
				if dep in variables:
					value_slots[i]    = variables[dep]
				else:
					mask_free_vars[i] = True

			output = np.full((len(assignment), *shape_output), True, dtype = "bool")

			for indices in np.ndindex(shape_output):
				value_slots[mask_free_vars] = np.array(indices)[position_free_vars]
				indexing                    = slice(len(assignment)), *indices
				output[indexing]            = assignment[:, vm.index(self.idx, value_slots)]

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
