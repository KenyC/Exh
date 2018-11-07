import numpy as np
from worlds import Universe
from utils import entails

class Alternatives():

	def __init__(self, prejacent, *fs):
		self.fs = fs
		self.p = prejacent


		self.n = max(v for f in fs for v in f.vars())

		self.u = Universe(self.n)

	def find_maximal_sets(universe, props):
		truthTable = universe.evaluate(*props)
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

	

		
