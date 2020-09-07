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


	def toggle_pound_smallest(n): 
		"""
		Maps the truth-values as follows (T: true, F: false, # : pound) 
		F#T
		->
		#FT

		Useful to convert connectives from weak to strong Kleene and vice-versa
		This function is its own inverse
		"""
		return  - 1 - n + 3 * (n == 1) # this complicated construct is meant to work with both np array and ordinary int

	def toggle_pound_greatest(n): 
		"""
		Maps the truth-values as follows (T: true, F: false, # : pound) 
		F#T
		->
		FT#

		Useful to convert connectives from weak to strong Kleene and vice-versa
		This function is its own inverse
		"""
		return 1 - n - 2 * (n == -1) # this complicated construct is meant to work with both np array and ordinary int