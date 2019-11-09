import numpy as np
from IPython.display import Math, display, HTML

def getAssignment(n):
	iterator = [np.array(2**(n-i-1)*(2**(i) * [False] + 2**(i) * [True]), dtype = "bool") for i in range(n)]
	return np.transpose(np.stack(iterator))

def entails(a, b):
	return np.all(np.logical_or(np.logical_not(a), b))

def remove_doubles(fs):

	toReturn = []

	for f in fs:
		if all(f != g for g in toReturn):
			toReturn.append(f)

	return toReturn

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


def jprint(*args):
	display(HTML(" ".join(list(map(str, args)))))