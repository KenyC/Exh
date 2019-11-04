import numpy as np
from IPython.display import Math, display, HTML


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

def jprint(*args):
	display(HTML(" ".join(list(map(str, args)))))