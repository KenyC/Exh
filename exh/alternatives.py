"""
This module offers a collection of tools to work with alternatives:
compute alternatives of a formula, find maximal consistent sets, etc.
"""
import numpy as np
from itertools import product
import copy

from . import exhaust
from . import options
from exh.prop       import And, Or, Not, Formula, Pred
from exh.fol        import Universal, Existential
from exh.utils      import entails, remove_doubles



constructors = {"And":         lambda pre: And(*pre.children),
				"Or":          lambda pre: Or(*pre.children),
				"Not":         lambda pre: Not(*pre.children),
				"Exh":         lambda pre: exhaust.Exh(pre.children[0], alts = pre.alts),
				"Existential": lambda pre: Existential(pre.qvar, pre.children[0]),
				"Universal":   lambda pre: Universal(pre.qvar, pre.children[0])}





def find_maximal_sets(universe, props, variables = None):
	"""
	Given a set of worlds and a set of propositions, this method returns the maximal sets of propositions that are consistent with one another

	Algorithm:
	focus on the sets S of proposition which are all the propositions true in some world
	return the maximal sets of S

	Arguments:
		universe (Universe)
		props (list[Formula]) -- set of propositions to compute the maximal sets of

	"""
	kwargs       = {} if variables is None else {"variables" : variables}
	truth_table  = universe.evaluate(*props, no_flattening = True, **kwargs)
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

	return np.stack(maximal_sets) #if maximal_sets else np.full((0, 0), True, dtype = "bool")





def simplify_alt(alt):
	"""Performs simple heuristics to simplify a formula: such as "A or A" is "A" ; "A and A" is "A" """
	if isinstance(alt, Or) or isinstance(alt, And):
		if len(alt.children) == 2 and alt.children[0] == alt.children[1]:
			return alt.children[0]
	return alt

def simplify_alts(alts):
	"""Applies "simplify_alt" to a list"""
	return list(map(simplify_alt, alts))





def alt_aux(p, scales, subst):
	"""Return alternatives to a formula following a Sauerland-esque algorithm"""
	# in case the prejacent is an Exh with stipulated alternatives, just return that
	if isinstance(p, Pred):
		return [p]

	if isinstance(p, exhaust.Exh):
		all_alternatives = [p.prejacent]
		all_alternatives.extend(p.alts)
		exh_alternatives = [exhaust.Exh(alt, alts = all_alternatives[:i] + all_alternatives[i + 1:]) 
		                    for i, alt in enumerate(all_alternatives)]
		return exh_alternatives


	# Scales that the current node participates in
	rel_scale = set(type_f for s in scales if any(isinstance(p, type_f) for type_f in s) 
	                       for type_f in s if not isinstance(p, type_f))

	children_alternative = [alt_aux(child, scales, subst) for child in p.children]

	# The alternatives are replaced by copies
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

def alt(p, scales = [], subst = False):
	"""Simplifies the result of alt_aux for efficiency"""
	return remove_doubles(simplify_alts(alt_aux(p, scales, subst)))







	
