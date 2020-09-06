import enum

class TVal(enum.IntEnum):
	"""
	Enumeration for truth-values.
	The int values associated to the truth-values constant are chosen so that typical connectives translate to easy arithmetic operations: 
	weak Kleene "and" is minimum
	"""
	true  = 1
	false = -1
	pound = 0


	def swap(n): 
		"""
		Maps n to:
		0  -> -1
		-1 -> 0
		1  -> 1
		Useful to convert connectives from weak to strong Kleene and vice-versa
		"""
		return n + (n < 1) * (- 1 - 2 * n) # this complicated construct is meant to work with both np array and ordinary int