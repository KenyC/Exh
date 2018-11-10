import numpy as np
class Formula:

	def __init__(self, typeF, *child):
		self.children = child
		self.type = typeF

	def __and__(self, other):
		return Formula("and", self, other)

	def __or__(self, other):
		return Formula("or", self, other)

	def __invert__(self):
		return Formula("not", self)

	def display(self):
		if self.type == "var":
			return "A{}".format(self.children[0])
		elif self.type == "not":
			return "not[{}]".format(self.children[0].display())
		elif self.type == "exh":
			return "exhp[{}]".format(self.children[0].display())
		else:
			return "{a} {type} {b}".format(type = self.type, a = self.parenthesis(self.children[0]).format(self.children[0].display()),
															 b = self.parenthesis(self.children[1]).format(self.children[1].display()),)

	def parenthesis(self, child):
		return "{}" if self.type == child.type or (len(child.children) <= 1) else "[{}]"

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
			else:
				return self.eq(other)
			

	def evaluate(self, assignment):

		if self.type == "var":
			return assignment[:, self.children[0]]
		elif self.type == "and":
			return np.logical_and(self.children[0].evaluate(assignment), self.children[1].evaluate(assignment))
		elif self.type == "or":
			return np.logical_or(self.children[0].evaluate(assignment), self.children[1].evaluate(assignment))
		elif self.type == "not":
			return np.logical_not(self.children[0].evaluate(assignment))

	def vars(self):

		if self.type == "var":
			return self.children
		else:
			return [x for c in self.children for x in c.vars()]

def Var(number):
	return Formula("var", number)


a = Var(0)
b = Var(1)
c = Var(2)

f1 = a & b & ~c
f2 = a | (b & c)

