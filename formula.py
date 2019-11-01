import numpy as np
import utils
from collections import defaultdict
import itertools

from vars import VarManager
import options



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

	def display(self):

		def paren(typeF, child):
			if (typeF == child.type) or (child.type == "var") or (child.type == "not"):
				return str(child)
			else:
				return "({})".format(child)

		if self.type == "not":
			return "not[{}]".format(self.children[0].display())
		elif self.type == "exh":
			return "exhp[{}]".format(self.children[0].display())
		else:
			return "{a} {type} {b}".format(type = self.type, a = paren(self.type, 
																		self.children[0]),
															 b = paren(self.type, 
															 			self.children[1]))

	def __str__(self):
		return self.display()

	def __repr__(self):
		return self.display()

	def __eq__(self, other):
		if self.type == other.type:
			if self.type == "var" or self.type == "neg":
				return self.children[0] == other.children[0]
			elif self.type == "or" or self.type == "and":
				return (self.children[0] == other.children[0] and self.children[1] == other.children[1]) or (self.children[0] == other.children[1] and self.children[1] == other.children[0])
			elif self.type == "exh":
				return self.children[0] == self.children[0]

	def evaluate(self, **kwargs):

		if "vm" in kwargs:
			vm = kwargs["vm"]
		else: 
			vm = self.vm


		if "assignment" in kwargs:
			assignment = kwargs["assignment"]
		else:
			assignment = np.full(vm.n, True)

			for var, val in kwargs.items():
				if var in vm.names:
					idx = vm.names[var]
				else:
					continue

				deps = vm.preds[idx]

				for t in itertools.product(range(options.dom_quant), repeat = len(deps)):
					i = vm.index(idx, **{key: val for key, val in zip(deps, t)})
					assignment[i] = utils.get(val, t)

			assignment = assignment[np.newaxis, :]


		to_return = self.evaluate_aux(assignment, vm)

		if all(dim == 1 for dim in to_return.shape):
			return np.asscalar(to_return)
		else:
			return to_return


	def evaluate_aux(self, assignment, vm, variables = dict()):
	

		if self.type == "and":
			return np.logical_and(self.children[0].evaluate_aux(assignment, vm, variables),
								  self.children[1].evaluate_aux(assignment, vm, variables))
		elif self.type == "or":
			return np.logical_or(self.children[0].evaluate_aux(assignment, vm, variables),
								  self.children[1].evaluate_aux(assignment, vm, variables))
		elif self.type == "not":
			return np.logical_not(self.children[0].evaluate_aux(assignment, vm, variables))

		return "ohohoo"


	def vars(self):
		self.vm = VarManager.merge(*[c.vars() for c in self.children])
		self.vm.linearize()
		return self.vm



# def Var(number):
# 	return Formula("var", number)


class Var(Formula):

	def __init__(self, number, depends_on = None, name = None):
		self.deps = depends_on if depends_on is not None else set()
		self.name = name
		super(Var, self).__init__("var", number)

	def display(self):
		if self.deps:
			dep_string = "({})".format(",".join(list(self.deps)))
		else:
			dep_string = ""
		
		if self.name is None:
			return "A{}".format(self.children[0]) + dep_string
		else:
			return self.name + dep_string

	def depends_on(self, var):
		self.deps.add(var)

	def __call__(self, *variables):
		for var in variables:
			self.depends_on(var)

		return self

	def evaluate_aux(self, assignment, vm, variables = dict()):
		return assignment[:, vm.index(self.idx, **variables)]

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

