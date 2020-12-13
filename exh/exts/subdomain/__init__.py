"""
This module deals with making subdomain alternatives for existentials
"""
import numpy      as np
import exh.fol    as q
import exh.utils  as utils

class SubdomainExistential(q.Quantifier):
	"""docstring for SubdomainExistential"""
	verbose = True
	plain_symbol = "\u2203c"
	latex_symbol = r"\exists_C"

	def __init__(self, quant_var, scope, domain = None, mask = None):
		super(SubdomainExistential, self).__init__(quant_var = quant_var, scope = scope, domain = domain)
		if mask is None:
			mask = np.full(self.domain.n, True)
		self.mask = mask

		if self.verbose:
			self.plain_symbol = "\u2203" + "".join("\u02da" if bit else "\u02d9" for bit in self.mask)
			self.latex_symbol = "\u2203_{{{}}}".format("".join(r"\circ" if bit else "." for bit in self.mask))

	def fun(self, results):
		return np.max(results[self.mask], axis = 0)

	def __eq__(self, other):
		if self.__class__ is other.__class__:
			return self.qvar == other.qvar and np.all(self.mask == other.mask) and self.children[0] == other.children[0] 
		return False

	def lower_alternatives(self):
		n_true_mask = np.sum(self.mask)
		for line in utils.getAssignment(n_true_mask)[1:-1]:
			mask = self.mask.copy()
			mask[self.mask] = line
			yield SubdomainExistential(self.qvar, self.scope, self.domain, mask)

	def all_alternatives(self):
		for line in utils.getAssignment(len(self.mask))[1:]:
			if np.all(line == self.mask):
				pass
			else:
				yield SubdomainExistential(self.qvar, self.scope, self.domain, line)


class SubdomainScale:
	"""docstring for SubdomainScale"""
	def __init__(self, sub_only = True):
		super(SubdomainScale, self).__init__()
		self.sub_only = sub_only

	def alternatives_to(self, prejacents):
		original = prejacents[0]
		if isinstance(original, SubdomainExistential):
			alternatives = SubdomainExistential.lower_alternatives if self.sub_only else SubdomainExistential.all_alternatives
			return [alt for prejacent in prejacents for alt in alternatives(prejacent)]
		else:
			return []
		
sub_scale = SubdomainScale(True)
dom_scale = SubdomainScale(False)

def Ec_(var, domain = None, mask = None):
	return q.C(lambda scope: SubdomainExistential(var, scope, domain = domain, mask = mask))

Ec_x = Ec_("x")
Ec_y = Ec_("y")
Ec_z = Ec_("z")