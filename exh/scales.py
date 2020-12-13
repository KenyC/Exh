"""
The classes below find alternatives repalcing the root operator by a scalemate ; they preserve the overall structure of the formula
"""

class Scales:
	def __add__(self, other):
		if isinstance(other, ListScales):
			return other + self
		else: 
			return ListScales([self, other])

class SimpleScales(Scales):
	"""
	This class uses the method of "alternative_to" to generate scalemates. It only looks at the type of the prejacent to find its scalemates.
	As such, it cannot do content-based alternative subsitution (e.g. "more than 6" to "more than 7", since both have the same type)
	But it is easy to define since it only demands its scales passed as simple list
	"""

	def __init__(self, scales):
		"""
		Arguments:
		    - scales (list[set[type]]) : a list of scales (seen as sets of types)
		"""
		self.scales = scales


	def alternatives_to(self, prejacents):
		"""
		From a list of prejacents assumed to have the same root operator Op, compute a set of alternatives replacing Op with scalemates

		Arguments:
		    - prejacents (list[Formula]) : a list of formulas
		"""
		if prejacents:
			# Find the scalemates of the prejacent
			example = prejacents[0] # take the first element to find the type of the formulas
			rel_scale = set(type_f for s in self.scales if any(isinstance(example, type_f) for type_f in s) 
			                       for type_f in s if not isinstance(example, type_f))

			# we now need to include scalar replacements
			scalar_alts = []
			for scale_mate in rel_scale:
				for alt_root_fixed in prejacents:
					scalar_alts.append(scale_mate.alternative_to(alt_root_fixed))
			return scalar_alts
		else:
			return []

	def __repr__(self):
		return "SimpleScales({scales})".format(self.scales.__repr__())

class ListScales(Scales):
	"""
	This class takes a list of scales and apply all of them
	"""
	def __init__(self, scales):
		self.scales = scales

	def alternatives_to(self, prejacents):
		return [alt for scale in self.scales for alt in scale.alternatives_to(prejacents)]

	def __add__(self, other):
		if isinstance(other, ListScales):
			return ListScales(self.scales + other.scales)
		else:
			return ListScales(self.scales + [other])