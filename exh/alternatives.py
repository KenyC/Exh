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


############################ MAXIMAL SETS ##############################################


def find_maximal_sets(universe, props, variables = None):
	"""
	Given a set of worlds and a set of propositions, this method returns the maximal sets of propositions that are consistent with one another

	Algorithm:
	focus on the sets S of proposition which are all the propositions true in some world
	return the maximal sets of S

	Arguments:
		universe (Universe)
		props    (list[Formula]) -- set of propositions to compute the maximal sets of

	Returns:
		np.array[bool]           -- returned_value[i, j] is True iff i-th maximal set contains j-th proposition

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




############################ ALTERNATIVE GENERATION ##############################################
"""
*alts_aux* performs the automatic generation of alternatives
*alts* adds on top of this simplification of the set of alternatives using braindead heuristics
"""




# @profile
def alt_aux(p, scales, subst):
	"""
	Return alternatives to a formula following a Sauerland-esque algorithm. 
	Specifically, an alternative is anything which can be obtained from the prejacent by sub-constituent replacement ("A" is an alternative to "A or B"), scale replacement ("a or b" is an alternative to "a and b")
	
	Arguments:
		p      (Formula)           -- prejacent
		scales (list[tuple[class]])-- the list of scales in the lexicon
		subst  (bool)              -- whether to take subconstituent alternatives

	Returns:
		list[Formula] -- the alternatives

	"""

	# A predicate has no alternatives
	if isinstance(p, Pred):
		return [p]

	# in case the prejacent is an Exh, its alternative are either stipulated or already computed as "p.alts"
	# So the returned set of alternatives is just {Exh(alt) | alt \in p.alts}
	if isinstance(p, exhaust.Exh):
		all_alternatives = [p.prejacent]
		all_alternatives.extend(p.alts)

		
		exh_alternatives = [p]
		exh_alternatives.extend(
			[exhaust.Exh(alt, alts = all_alternatives[:i] + all_alternatives[i + 1:]) 
		                    for i, alt in enumerate(all_alternatives) if i != 0 # <--- trick: we don't recompute exhaustification of the prejacent
			]
		) 
		# exh_alternatives = [exhaust.Exh(alt, alts = all_alternatives[:i] + all_alternatives[i + 1:]) 
		#                     for i, alt in enumerate(all_alternatives)]
		return exh_alternatives

	# GENERAL CASE:


	# Find the scalemates of the prejacent
	rel_scale = set(type_f for s in scales if any(isinstance(p, type_f) for type_f in s) 
	                       for type_f in s if not isinstance(p, type_f))

	# Recursively obtain the alternatives of the children nodes of the prejacent 
	children_alternative = [alt_aux(child, scales, subst) for child in p.children]


	root_fixed_alts = []
	# For every choice of an alternative to a child (C1 x C2 x ... x Cn where Ci are the children's alternatives)
	for t in product(*children_alternative):
		# To avoid problems, the prejacent is copied
		to_append = copy.copy(p)
		to_append.children = t

		# Because exhaust will need to perform computation at initialization, we need to reinitialize. (<= Not sure if this is necessary given that the case Exh is already dealt with)
		to_append.reinitialize()#constructors[p.type](to_append)
		root_fixed_alts.append(to_append)
	# "root_fixed_alts" now contains all alternatives to the current formula that keep the root node the same 
	# e.g. p = a | (b & c) => root_fixed_alts = [a | b, a | c, a | (b | c), a | (b & c)]

	# we now need to include scalar replacements
	scalar_alts = []
	for scale_mate in rel_scale:
		for child in root_fixed_alts:
			scalar_alts.append(constructors[scale_mate.__name__](child))

	

	if subst and p.subst: # if sub-constituent are alternatives, add every element of child_alts 
		return root_fixed_alts + scalar_alts + [alt for child_alts in children_alternative for alt in child_alts]
	else:
		return root_fixed_alts + scalar_alts

# @profile
def alt(p, scales = [], subst = False):
	"""
	Simplifies the result of alt_aux for efficiency

	1) Simplify trivial alternatives: A or A -> A, B and B -> B
	2) Remove duplicate alternatives: {A, B, B, A or B} -> {A, B, A or B}
	"""
	return remove_doubles(simplify_alts(alt_aux(p, scales, subst)))
	# return alt_aux(p, scales, subst)




def simplify_alt(alt):
	"""Performs simple heuristics to simplify a formula, namely "A or A" is "A" ; "A and A" is "A" """
	if isinstance(alt, Or) or isinstance(alt, And):
		if len(alt.children) == 2 and alt.children[0] == alt.children[1]:
			return alt.children[0]
	return alt

def simplify_alts(alts):
	"""Applies "simplify_alt" to a list"""
	return list(map(simplify_alt, alts))



	
