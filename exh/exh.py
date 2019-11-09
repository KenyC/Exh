import numpy as np

import exh.options as options
from exh.utils import jprint

import exh.alternatives as alternatives
from exh.worlds import Universe
from exh.vars import VarManager
from exh.formula import Formula

class Exhaust:
	
	def __init__(self, prejacent, alts = None, scales = options.scales, subst = options.sub):
		self.p = prejacent
		if alts is None:
			self.alts = alternatives.Alternatives.alt(prejacent, scales = scales, subst = subst)
		else:
			self.alts = alts

		self.incl = False
		self.excl = False

		self.vm = VarManager.merge(prejacent.vm, *[alt.vm for alt in self.alts])
		self.u = Universe(vm = self.vm)


	def innocently_excludable(self):

		evalSet = [~f for f in self.alts]

		worldsPrejacent = self.u.evaluate(self.p).reshape(2 ** self.u.n)
		uPrejacent = self.u.restrict(worldsPrejacent)

		if evalSet:
			maximalSets = alternatives.Alternatives.find_maximal_sets(uPrejacent, evalSet)
			self.maximalExclSets = [[evalSet[i].children[0] for i,b in enumerate(setE) if b] for setE in maximalSets]

			self.innocently_excl_indices = np.prod(maximalSets, axis = 0, dtype = "bool")
			self.innocently_excl = [f for i,f in enumerate(self.alts) if self.innocently_excl_indices[i] == True]
		else:
			self.maximalExclSets = []
			self.innocently_excl = []

		self.excl = True
		return self.innocently_excl

	def innocently_includable(self):

		if not self.excl:
			raise ValueError("Exclusion has not been applied yet.")

		evalNegSet = [~f for f in self.innocently_excl] + [self.p]
		evalPosSet = [f for i,f in enumerate(self.alts) if not self.innocently_excl_indices[i]]

		worldsStengthenedPrejacent = np.prod(self.u.evaluate(*evalNegSet), axis = 1,dtype = "bool")
		uSPrejacent = self.u.restrict(worldsStengthenedPrejacent)
		
		if evalPosSet:
			maximalSets = alternatives.Alternatives.find_maximal_sets(uSPrejacent, evalPosSet)
			self.maximalInclSets = [[evalPosSet[i] for i,b in enumerate(setE) if b] for setE in maximalSets]
		
			self.innocently_incl_indices = np.prod(maximalSets, axis = 0, dtype = "bool")
			self.innocently_incl = [f for i,f in enumerate(evalPosSet) if self.innocently_incl_indices[i]]
		else:
			self.maximalInclSets = []
			self.innocently_incl = []

		self.incl = True
		return self.innocently_incl

	def diagnose(self):

		def colon_sep_fs(fs):
			str_fs = [str(f) for f in fs]
			return "; ".join(str_fs) 

		if self.excl:
			jprint("Maximal Sets (excl):")
			for excl in self.maximalExclSets:
				jprint("{" + colon_sep_fs(excl) + "}") 
			jprint()
			jprint("Innocently excludable:", colon_sep_fs(self.innocently_excl))

		if self.incl:
			jprint()
			jprint()
			jprint("Maximal Sets (incl):")
			for incl in self.maximalInclSets:
				jprint("{" + colon_sep_fs(incl) + "}") 
			jprint()
			jprint("Innocently includable:", colon_sep_fs(self.innocently_incl))
		jprint()

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

	# def display_aux(self):
	# 	return "exh[{}]".format(self.children[0].display())

	def evaluate_aux(self, assignment, vm, variables = dict()):

		evaluanda = [self.children[0]] + self.evalSet
		values = [f.evaluate_aux(assignment, vm, variables) for f in evaluanda]
	
		return np.min(np.stack(values), axis = 0)

	def get_alts(self):
		return self.e.alts


	def vars(self):
		self.vm = VarManager.merge(self.children[0].vm, *[alt.vm for alt in self.alts])
		return self.vm

	def diagnose(self):
		self.e.diagnose()

	def eq(self, other):
		return (other.type == "exh") and (self.children[0] == other.children[0])


	alts = property(get_alts)








