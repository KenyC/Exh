import numpy as np
from alternatives import Alternatives
from worlds import Universe
from formula import Formula
import options

class Exhaust:
	
	def __init__(self, prejacent, alts = None, scales = options.scales, subst = options.sub):
		self.p = prejacent
		if alts is None:
			self.alts = Alternatives.alt(prejacent, scales = scales, subst = subst)
		else:
			self.alts = alts

		self.n = max(v for f in self.alts for v in f.vars())
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


class Exh(Formula):
	
	def __init__(self, child, alts = None, scales = options.scales, subst = options.sub, ii = options.ii_on):
		self.e = Exhaust(child, alts, scales, subst)
		
		self.ieSet = self.e.innocently_excludable()

		if ii:
			self.iiSet = self.e.innocently_includable()
		else:
			self.iiSet = []
		

		self.evalSet = [~f for f in self.ieSet] + [f for f in self.iiSet]

		super(Exh, self).__init__("exh", child)

	def display(self):
		return "exh[{}]".format(self.children[0].display())

	def evaluate(self, assignment):
		uEval = Universe(len(assignment), assignment)

		return np.prod(uEval.evaluate(self.children[0], *self.evalSet), axis = 1, dtype = "bool")






