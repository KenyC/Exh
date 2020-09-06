import numpy as np
import itertools as it
import enum

import exh.utils          as utils
import exh.prop.formula   as bivalent
import exh.model.options  as options
from exh.exts.trivalence.model.truth import TVal

class ProjectionRules(enum.Enum):
	StrongKleene = 1   # undefined if true in some but not all supervaluations (i.e. pound truth-value is read as unknown)
	WeakKleene   = -1  # undefined if any element is undefined                 (i.e. pound truth-value is read as undefined)
	MiddleKleene = 0   # asymmetrid weak/strong Kleene logic (e.g. the logic underlying Schlenker's transparency theory)

class Formula(bivalent.Formula):
	"""
	Trivalent equivalent of Formule defined in the base package. 
	This class and the original Formula class should not be mixed and matched
	"""

	projection = ProjectionRules.StrongKleene

	def __init__(self, *args, **kwargs):
		super(Formula, self).__init__(*args, **kwargs)


	def __and__(self, other):
		""" Redefining __and__ with trivalent AND """
		return And(self, other)

	def __or__(self, other):
		""" Redefining __or__ with trivalent OR """
		return Or(self, other)

	def __invert__(self):
		""" Redefining __or__ with trivalent Not """
		return Not(self)


	def make_assignment_from_predicate_values(self, predicate_values, vm):
		"""
		This method is called when evaluate is called with predicates name (e.g. (a & b).evaluate(a = True, b = False))
		We override mother's method to ensure that created assignment of values are int by default		
		"""
		assignment = np.full(vm.n, TVal.true)

		for var, val in predicate_values.items():
			if var in vm.names:
				idx = vm.names[var]
			# else:
			# 	continue

			deps = vm.preds[idx]

			for t in it.product(range(options.dom_quant), repeat = deps):
				i = vm.index(idx, t)
				assignment[i] = utils.get(val, t)

		return assignment[np.newaxis, :]

	def copy(self):
		"""Creates copy of the object (overridden by children's classes)"""
		return Formula(*self.children)


class Operator(Formula, bivalent.Operator):
	"""
	Trivalent version of class Operator
	"""
	pass

class Not(Operator):
	no_parenthesis = True

	plain_symbol = "not"
	latex_symbol = r"\neg"

	fun_ = lambda x: np.squeeze(- x, axis = 0)

	"""docstring for Not"""
	def __init__(self, child):
		super(Not, self).__init__(Not.fun_, child)


# Strong Kleene operators

class StrongKleene:
	"""
	Container for Strong Kleene binary connectives.
	can be used in a "with" environment for temporary swap of projection rules
	"""
	def __enter__(self):
		self.previous_rules = Formula.projection
		Formula.projection = ProjectionRules.StrongKleene

	def __exit__(self, type, value, traceback):
		Formula.projection = self.previous_rules
		
	class And(Operator):
		"""Strong Kleene 'and' """
		plain_symbol = "and_SK"
		latex_symbol = r"\land_{SK}"

		def fun_(values):
			return np.min(values, axis = 0)

		def __init__(self, *children):
			super(StrongKleene.And, self).__init__(StrongKleene.And.fun_, *children)


	class Or(Operator):
		""" Strong Kleene 'or' """
		plain_symbol = "or_SK"
		latex_symbol = r"\lor_{SK}"
		
		def fun_(values):
			return np.max(values, axis = 0)

		def __init__(self, *children):
			super(StrongKleene.Or, self).__init__(StrongKleene.Or.fun_, *children)

# Weak Kleene operators

class WeakKleene:

	"""
	Container for Strong Kleene binary connectives.
	can be used in a "with" environment for temporary swap of projection rules
	"""
	def __enter__(self):
		self.previous_rules = Formula.projection
		Formula.projection = ProjectionRules.WeakKleene

	def __exit__(self, type, value, traceback):
		Formula.projection = self.previous_rules

	class And(Operator):
		"""Weak Kleene 'and' """
		plain_symbol = "and_WK"
		latex_symbol = r"\land_{WK}"

		def fun_(values):
			return TVal.swap_pound_smallest(np.min(TVal.swap_pound_smallest(values), axis = 0))

		def __init__(self, *children):
			super(WeakKleene.And, self).__init__(WeakKleene.And.fun_, *children)


	class Or(Operator):
		""" Weak Kleene 'or' """
		plain_symbol = "or_WK"
		latex_symbol = r"\lor_{WK}"
		
		def fun_(values):
			return TVal.swap_pound_greatest(np.max(TVal.swap_pound_greatest(values), axis = 0))


		def __init__(self, *children):
			super(WeakKleene.Or, self).__init__(WeakKleene.Or.fun_, *children)

"""
The simpler named methods below always isntantiate an object based on th current rules of projection in Formula.projection 
"""

def And(*args, **kwargs):
	if Formula.projection == ProjectionRules.StrongKleene:
		return StrongKleene.And(*args, **kwargs)
	elif Formula.projection == ProjectionRules.WeakKleene:
		return WeakKleene.And(*args, **kwargs)
	else:
		raise Exception("Not implemented yet!")

def Or(*args, **kwargs):
	if Formula.projection == ProjectionRules.StrongKleene:
		return StrongKleene.Or(*args, **kwargs)
	elif Formula.projection == ProjectionRules.WeakKleene:
		return WeakKleene.Or(*args, **kwargs)
	else:
		raise Exception("Not implemented yet!")
