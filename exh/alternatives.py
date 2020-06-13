"""
This module offers a collection of tools to work with alternatives:
compute alternatives of a formula, find maximal consistent sets, etc.
"""
import numpy as np
from itertools import product
import copy

from . import exh as exhaust
import exh.options as options
from exh.formula import And, Or, Not, Formula, Pred
from exh.quantifier import Universal, Existential
from exh.utils import entails, remove_doubles



constructors = {"And":         lambda pre: And(*pre.children),
				"Or":          lambda pre: Or(*pre.children),
				"Not":         lambda pre: Not(*pre.children),
				"Exh":         lambda pre: exhaust.Exh(pre.children[0], alts = pre.alts),
				"Existential": lambda pre: Existential(pre.qvar, pre.children[0]),
				"Universal":   lambda pre: Universal(pre.qvar, pre.children[0])}





"""
Given a set of worlds and a set of propositions, this method returns the maximal sets of propositions that are consistent with one another
Algorithm:
focus on the sets S of proposition which are all the propositions true in some world
return the maximal sets of S
"""
def find_maximal_sets(universe, props):
	truth_table = universe.evaluate(*props)
	maximal_sets = []

	# for every world,
	for s in truth_table:

		# test if the set of true proposition in that world is smaller than any of the current maximal sets
		# if yes, go on to the next world
		# if no, remove any smaller set from maximal set and insert
		if any(entails(s, m) for m in maximal_sets):
			continue
		else:
			maximal_sets = [m for m in maximal_sets if not entails(m, s)]
			maximal_sets.append(s)

	
	return np.array(maximal_sets, dtype = "bool")

# Performs simple heuristics to simplify a formula: such as "A or A" is "A" ; "A and A" is "A"
def simplify_alt(alt):
	if isinstance(alt, Or) or isinstance(alt, And):
		if len(alt.children) == 2 and alt.children[0] == alt.children[1]:
			return alt.children[0]
	return alt

# Applies "simplify_alt" to a list
def simplify_alts(alts):
	return list(map(simplify_alt, alts))


"""
Return alternatives to a formula following a Katzirian algorithm
"""
def alt_aux(p, scales, subst):

	if isinstance(p, Pred):
		return [p]

	# Scales that the current node participates in
	rel_scale = set(type_f for s in scales if any(isinstance(p, type_f) for type_f in s) 
	                       for type_f in s if not isinstance(p, type_f))

	children_alternative = [alt_aux(child, scales, subst) for child in p.children]

	children_replacement = []
	for t in product(*children_alternative):
		to_append = copy.copy(p)
		to_append.children = t

		# Because exhaust will need to perform computation at initialization, we need to reinitialize.
		to_append.reinitialize()#constructors[p.type](to_append)
		children_replacement.append(to_append)

	scale_replacement = []
	for scale_mate in rel_scale:
		for child in children_replacement:
			scale_replacement.append(constructors[scale_mate.__name__](child))

	if subst and p.subst:
		return children_replacement + scale_replacement + [alt for child_alts in children_alternative for alt in child_alts]
	else:
		return children_replacement + scale_replacement

# Simplifies the result of alt_aux for efficiency
def alt(p, scales = [], subst = False):
	return remove_doubles(simplify_alts(alt_aux(p, scales, subst)))







	
