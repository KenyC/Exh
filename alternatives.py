import numpy as np
from worlds import Universe
from formula import Formula
import exh
from utils import entails, remove_doubles
from itertools import product


d = {"and": lambda l: Formula("and", *l), "or": lambda l: Formula("or", *l), "not": lambda l: Formula("not", *l),"exh": lambda l: exh.Exh(l[0])}

class Alternatives():

	def __init__(self, prejacent, *fs):
		self.fs = fs
		self.p = prejacent


		self.n = max(v for f in fs for v in f.vars())

		self.u = Universe(self.n)

	def find_maximal_sets(universe, props):
		truthTable = universe.evaluate(*props)
		print(truthTable)
		maximalSets = []

		for s in truthTable:

			toInsert = True

			for i, m in enumerate(maximalSets):
				
				if entails(s, m):
					toInsert = False
					break
				elif entails(m, s):
					del maximalSets[i]
				
			if toInsert:
				maximalSets.append(s)
		
		return np.array(maximalSets, dtype = "bool")


	def alt_aux(p, scales = [], subst = False):

		if p.type == "var":
			return [p]

		relScale = set(t for s in scales if p.type in s for t in s)
		relScale.add(p.type)

		childrenAlternative = [Alternatives.alt_aux(child, scales, subst) for child in p.children]
		toReturn = [d[s](bigProd) for s in relScale for bigProd in product(*childrenAlternative)]

		return toReturn + ([alt for child in childrenAlternative for alt in child] if subst else [])

	def alt(p, scales, subst):
		return remove_doubles(Alternatives.alt_aux(p, scales, subst))





	

		
