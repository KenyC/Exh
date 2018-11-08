import numpy as np
from alternatives import Alternatives
from worlds import Universe
import options

class Exhaust:
	
	def __init__(self, prejacent, alts = None):
		self.p = prejacent
		if alts is None:
			self.alts = Alternatives.alt(prejacent, scales = options.scales, subst = options.sub)
		else:
			self.alts = alts

		self.n = max(v for f in alts for v in f.vars())
		self.u = Universe(self.n + 1)

	def innocently_excludable(self):

		evalSet = [~f for f in self.alts]

		worldsPrejacent = self.p.evaluate(self.u.worlds)
		uPrejacent = self.u.restrict(worldsPrejacent)

		maximalSets = Alternatives.find_maximal_sets(uPrejacent, evalSet)

		self.innocently_excl_indices = np.prod(maximalSets, axis = 0, dtype = "bool")
		self.innocently_excl = [f for i,f in enumerate(self.alts) if self.innocently_excl_indices[i] == True]

		return self.innocently_excl

	def innocently_includable(self):

		evalNegSet = [~f for f in self.innocently_excl] + [self.p]
		evalPosSet = [f for i,f in enumerate(self.alts) if self.innocently_excl_indices[i] == False]

		worldsStengthenedPrejacent = np.prod(self.u.evaluate(*evalNegSet), axis = 1,dtype = "bool")
		uSPrejacent = self.u.restrict(worldsStengthenedPrejacent)
		
		maximalSets = Alternatives.find_maximal_sets(uSPrejacent, evalPosSet)
	
		self.innocently_incl_indices = np.prod(maximalSets, axis = 0)
		self.innocently_incl = [f for i,f in enumerate(evalPosSet) if self.innocently_incl_indices[i] == True]

		return self.innocently_incl


