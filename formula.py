import numpy as np
from vars import VarManager
from collections import defaultdict
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
			if (typeF == child.type) or (child.type == "var"):
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

	def evaluate(self, assignment, vm = None):

		# if self.type == "var":
		# 	return assignment[:, self.children[0]]
		# elif self.type == "and":
		# 	return np.logical_and(self.children[0].evaluate(assignment), self.children[1].evaluate(assignment))
		# elif self.type == "or":
		# 	return np.logical_or(self.children[0].evaluate(assignment), self.children[1].evaluate(assignment))
		# elif self.type == "not":
		# 	return np.logical_not(self.children[0].evaluate(assignment))

		return self.evaluate_aux(assignment, vm = None)


	def evaluate_aux(self, assignment, variables = dict(), vm = None):

		if vm is None:
			vm = self.vars()


		if self.type == "and":
			return np.logical_and(self.children[0].evaluate_aux(assignment, variables, vm),
								  self.children[1].evaluate_aux(assignment, variables, vm))
		elif self.type == "or":
			return np.logical_or(self.children[0].evaluate_aux(assignment, variables, vm),
								  self.children[1].evaluate_aux(assignment, variables, vm))
		elif self.type == "not":
			return np.logical_not(self.children[0].evaluate_aux(assignment, variables, vm))

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

	def evaluate_aux(self, assignment, variables, vm):
		idx = self.children[0]
		deps = vm.preds[idx]
		# print("This is relevant", idx, variables)
		return assignment[:, idx + sum(variables[dep] * (options.dom_quant ** i)   for i, dep in enumerate(deps) if dep in variables)]

	def vars(self):
		self.vm = VarManager({self.children[0]: self.deps})
		return self.vm

		




a = Var(0, name = "a")
b = Var(1, name = "b")
c = Var(2, name = "c")

f1 = a & b & ~c
f2 = a | b & c

