import numpy as np
from alternatives import Alternatives
from worlds import Universe

class Exhaust:
	
	def __init__(self, prejacent, alts = None):
		self.p = prejacent
		self.alts = alts

		self.n = max(v for f in alts for v in f.vars())
		self.u = Universe(self.n + 1)

	def innocently_excludable(self):

		evalSet = [~f for f in self.alts]

		worldsPrejacent = self.p.evaluate(self.u.worlds)
		uPrejacent = self.u.restrict(worldsPrejacent)

		maximalSets = Alternatives.find_maximal_sets(uPrejacent, evalSet)

		self.innocently_excl_indices = np.prod(maximalSets, axis = 0)
		self.innocently_excl = [f for i,f in enumerate(self.alts) if self.innocently_excl_indices[i] == True]

		return self.innocently_excl

