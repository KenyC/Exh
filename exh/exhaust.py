import numpy as np

# This is a circular import ; better import it at runtime
import exh.alternatives as alternatives
import exh.model        as model
import exh.prop         as prop
import exh.scales       as scale

from exh.utils import jprint
import exh.options as options



class Exhaust:
	"""
	This class orchestrates the computation of exhaustification.
	It computes the alternatives, if they are not provided ; it performs IE and II on them

	Attributes:
		p    (Formula)         -- the prejacent
		alts (list[Formula])   -- the alternatives
		incl (bool)            -- whether IE exhaustification has been computed yet
		incl (bool)            -- whether II exhaustification has been computed yet
		vm   (VariableManager) -- variable manager for prejacent & alternatives
		u    (Universe)        -- universe with all corresponding logical possibilities
	"""
	
	
	def __init__(self, prejacent, alts = None, scales = None, subst = None, extra_alts = []):
		"""
		Arguments
			- prejacent (Formula)       -- the prejacent
			- alts      (list[Formula]) -- stipulated alternatives. If None, alternatives are computed automatically
			- scales                    -- the scales used to compute automatic alternatives
			- subst     (bool)          -- whether subconstituent alternatives should be used
			- extra_alts(list[Formula]) -- if alternatives are computed automatically, add to the already computed alternatives some stipulated ones.
		"""
		# Defining default options dynamically so that users can change options on the fly
		if scales is None:
			if isinstance(options.scales, list):
				scales = scale.SimpleScales(options.scales)
			else:
				scales = options.scales
		elif isinstance(scales, list):
			scales = scale.SimpleScales(scales)

		if subst is None:
			subst = options.sub

		if alts is None: # if no alternative is given, compute them automatically
			self.alts = alternatives.alt(prejacent, scales = scales, subst = subst)
		else:
			self.alts = alts
		self.alts += extra_alts

		self.p = prejacent

		# If there are free variables in the prejacent or the alternatives, they must be saturated with dummy values 
		self.free_vars = set(self.p.free_vars)
		for alt in self.alts:
			self.free_vars.union(set(alt.free_vars))

		self.dummy_vals = {var: 0 for var in self.free_vars}

		self.incl = False
		self.excl = False

		self.vm = model.VarManager.merge(prejacent.vm, *(alt.vm for alt in self.alts))
		self.u  = model.Universe(vm = self.vm)


	def innocently_excludable(self):

		evalSet = [~f for f in self.alts]
		worldsPrejacent = np.squeeze(self.u.evaluate(self.p, no_flattening = True, 
		                                                     variables = self.dummy_vals), # give free variables dummy values
		                             axis = 1) 
		# We restrict ourselves to the worlds where the prejacent is True
		uPrejacent = self.u.restrict(worldsPrejacent)

		if evalSet and uPrejacent.n_worlds != 0:
			self.maximalExclSets         = alternatives.find_maximal_sets(uPrejacent, evalSet, variables = self.dummy_vals)
			self.innocently_excl_indices = np.prod(self.maximalExclSets, axis = 0, dtype = "bool") # innocently_excl_indices[i] is true iff the i-th proposition belongs to every maximal set
		else:
			self.maximalExclSets         = []
			self.innocently_excl_indices = []

		self.excl = True
		return self.innocently_excl_indices

	def innocently_includable(self):

		if not self.excl:
			raise ValueError("Exclusion has not been applied yet.")

		evalNegSet = [~f for f, excludable in zip(self.alts, self.innocently_excl_indices) if excludable] + [self.p]
		evalPosSet = [ f for f, excludable in zip(self.alts, self.innocently_excl_indices) if not excludable]

		worldsStengthenedPrejacent = np.prod(self.u.evaluate(*evalNegSet, no_flattening = True,
		                                                                  variables = self.dummy_vals),
		                                     axis = 1, 
		                                     dtype = "bool")

		# Restricting ourselves to the worlds where the prejacent is true and the negatable alternatives are false.
		uSPrejacent = self.u.restrict(worldsStengthenedPrejacent)
		
		if evalPosSet  and uSPrejacent.n_worlds != 0:
			maximalSets = alternatives.find_maximal_sets(uSPrejacent, evalPosSet, variables = self.dummy_vals)

			# The maximal sets refer to positions in the set of non-excludable alternatives ; we must convert this to position in the whole set of alternatives
			self.maximalInclSets = np.full((len(maximalSets), len(self.alts)), False, dtype = "bool")
			self.maximalInclSets[:, np.logical_not(self.innocently_excl_indices)] = maximalSets

			self.innocently_incl_indices = np.prod(self.maximalInclSets, axis = 0, dtype = "bool")
		else:
			self.maximalInclSets         = []
			self.innocently_incl_indices = []

		self.incl = True
		return self.innocently_incl_indices

	def diagnose(self, display = jprint):
		"""Diplay pertinent information regarding the results of the computation such as maximal sets, IE alternatives, II alternatives"""
		inline_sep = "; "
		list_sep   = "\n   - "

		def sep_fs(fs):
			str_fs = [str(f) for f in fs]
			n_fs   = len(str_fs)

			if n_fs > options.cutoff_inline_to_list:
				return list_sep + list_sep.join(str_fs)
			elif n_fs > 0:
				return inline_sep.join(str_fs)
			else:
				return "nothing"

		if self.excl:
			display("Maximal Sets (excl):")
			for excl in self.maximalExclSets:
				display("{" + inline_sep.join(list(map(str, self.extract_alts(excl)))) + "}") 
			display()
			display("Innocently excludable: ", sep_fs(self.innocently_excl))

		if self.incl:
			display()
			display()
			display("Maximal Sets (incl):")
			for incl in self.maximalInclSets:
				display("{" + inline_sep.join(list(map(str, self.extract_alts(incl)))) + "}") 
			display()
			display("Innocently includable: ", sep_fs(self.innocently_incl))
		display()

	@property
	def innocently_excl(self):
		return self.extract_alts(self.innocently_excl_indices)
	
	@property
	def innocently_incl(self):
		return self.extract_alts(self.innocently_incl_indices)
	

	def extract_alts(self, mask):
		return [alt for alt, included in zip(self.alts, mask) if included]	

class Exh(prop.Operator):
	"""
	This class wraps the class Exhaust into a Formula object, so that it can be evaluated like any Formula object

	Attributes:
		e (Exhaust) -- the object Exhaust that performs the actual computation
	"""

	plain_symbol = "Exh"
	latex_symbol = r"\textbf{Exh}"

	substitutable = False
	
	def __init__(self, child, alts = None, scales = None, subst = None, ii = None, extra_alts = []):
		self.e = Exhaust(child, alts, scales, subst, extra_alts)
		super(Exh, self).__init__(None, child)

		if ii is None:
			self.ii = options.ii_on
		else:
			self.ii = ii
		self.reinitialize()

	def reinitialize(self):
		self.e.p = self.prejacent
		self.ieSet = self.e.innocently_excludable()

		if self.ii:
			self.iiSet = self.e.innocently_includable()
		else:
			self.iiSet = []
		

		self.evalSet = [~f for f, excludable in zip(self.alts, self.ieSet) if excludable] + [f for f, includable in zip(self.alts, self.iiSet) if includable]



	def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):

		evaluanda = [self.children[0]] + self.evalSet
		values = [f.evaluate_aux(assignment, vm, variables) for f in evaluanda]
	
		return np.min(np.stack(values), axis = 0)


	@property
	def alts(self):
		return self.e.alts
	

	def vars(self):
		self.vm = model.VarManager.merge(self.children[0].vm, *[alt.vm for alt in self.alts])
		return self.vm

	def diagnose(self, *args, **kwargs):
		self.e.diagnose(*args, **kwargs)

	def __eq__(self, other):
		return isinstance(other, Exh) and (self.children[0] == other.children[0])

	@property
	def prejacent(self):
		return self.children[0]
	

	def copy(self):
		return Exh(self.prejacent, alts = self.alts)

	@classmethod
	def alternative_to(cls, other):
		return cls(other.children[0], alts = other.alts)










