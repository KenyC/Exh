import numpy as np
from itertools import product
import copy

from . import exh as exhaust
import exh.options as options
from exh.formula import Formula
from exh.quantifier import Universal, Existential
from exh.utils import entails, remove_doubles



constructors = {"and": lambda pre: Formula("and", *pre.children),
				"or": lambda pre: Formula("or", *pre.children),
				"not": lambda pre: Formula("not", *pre.children),
				"exh": lambda pre: exhaust.Exh(pre.children[0], alts = pre.alts),
				"some": lambda pre: Existential(pre.qvar, pre.children[0]),
				"all": lambda pre: Universal(pre.qvar, pre.children[0])}




class Alternatives():

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

	# Performs simple heuristics to simplify alternatives in the set ; A or A is A ; A and A is A
	def simplify_alt(alt):
		if alt.type == "or" or alt.type == "and":
			if alt.children[0] == alt.children[1]:
				return alt.children[0]
		return alt

	def simplify_alts(alts):
		return list(map(Alternatives.simplify_alt, alts))



	def alt_aux(p, scales, subst):

		if p.type == "var":
			return [p]

		rel_scale = set(t for s in scales if p.type in s for t in s if t != p.type)

		children_alternative = [Alternatives.alt_aux(child, scales, subst) for child in p.children]

		children_replacement = []
		for t in product(*children_alternative):
			to_append = copy.copy(p)
			to_append.children = t

			# Because exhaust performs computation at initialization, we need to recreate the object entirely.
			to_append = constructors[p.type](to_append)
			children_replacement.append(to_append)

		scale_replacement = []
		for scale_mate in rel_scale:
			for child in children_replacement:
				scale_replacement.append(constructors[scale_mate](child))

		if subst and p.type not in options.non_subst:
			return children_replacement + scale_replacement + [alt for child_alts in children_alternative for alt in child_alts]
		else:
			return children_replacement + scale_replacement

	def alt(p, scales = [], subst = False):
		return remove_doubles(Alternatives.simplify_alts(Alternatives.alt_aux(p, scales, subst)))





	

		
