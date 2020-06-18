"""
Not implemented yet!
"""

# from formula import Formula


class IteratorType:
	"""
	Iterator over all smallest nodes in the formula that are not of type "type_f"

	Example: in the formula ((a and b) or c) or (d or e), upon input type "or", the iterator returns:
	a and b, c, d, e
	"""
	def iterator_type(self, type_f = None):
		
		if type_f is None:
			type_f = self.__class__

		if isinstance(self, type_f):
			for child in self.children:
				for value in child.iterator_type(type_f):
					yield value
		else:
			yield self







