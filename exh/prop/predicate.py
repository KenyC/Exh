import exh.model.vars as var
import exh.utils      as utils

from .formula import Formula


############### PREDICATE CLASS ################

class Pred(Formula):
	"""
	Class for atomic proposition and predicate variable

	Attributes:
		name  -- name for display and evaluation
		arity -- for n-ary predicates, the number of variables that the predicate depends on
		deps  -- the name of the default variables that the predicate depends on
		(i.e. when no vars are specified, as in Ax > a, this is what the predicate depends on)
		idx   -- an integer that uniquely identifies the predicate
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
		"""Returns new predicate tied to the same index with different variable dependencies. If new number of variables is different from before, a warning is issues that worlds need to be rebuilt"""
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
		"""Specifies variable dependencies and arity of the predicate. Only used at initialization (use __call__ if not at initialization)"""

		# If arity is given, give default names to dependencies
		# e.g. a("x", "y", "z", "x1", "y1")
		if depends_on and isinstance(depends_on[0], int):
			self.arity = depends_on[0]
			self.deps = [var_name for _, var_name in zip(range(self.arity), utils.automatic_var_names())]
		else:
			self.arity = len(depends_on)
			self.deps = depends_on
