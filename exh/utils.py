import numpy as np
from IPython.display import Math, display, HTML
import itertools

"""
Returns all possible assignment of values to n independent boolean variables
"""
def getAssignment(n):
	iterator = [np.array(2**(n-i-1)*(2**(i) * [False] + 2**(i) * [True]), dtype = "bool") for i in range(n)]
	return np.transpose(np.stack(iterator))

def entails(a, b):
	return np.all(np.logical_or(np.logical_not(a), b))

"""
Returns a list of elements from iterable fs, without double values
"""
def remove_doubles(fs):

	toReturn = []

	for f in fs:
		if all(f != g for g in toReturn):
			toReturn.append(f)

	return toReturn

"""
Get value from multi-dimensional array "array" at indices specified by tuple "index_tuple"
"""
def get(array, index_tuple):

	to_return = array
	
	for index in index_tuple:
		to_return = to_return[index]

	return to_return

def add_functions_as_methods(fs):
	def decorator(Class):
		for f in fs:
			setattr(Class, f.__name__, f)
		return Class
	return decorator

"""
Replacement for print in IPython
"""
def jprint(*args):
	display(HTML(" ".join(list(map(str, args)))))


"""
Generator of default variable names
"""
def automatic_var_names():
	typical_names = ["x{}", "y{}", "z{}"]

	for x in itertools.chain([""], itertools.count()):
		for var in typical_names:
			yield var.format(x)
