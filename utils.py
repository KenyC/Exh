import numpy as np

def entails(a, b):
	return np.all(np.logical_or(np.logical_not(a), b))

def remove_doubles(fs):

	toReturn = []

	for f in fs:
		if all(f != g for g in toReturn):
			toReturn.append(f)

	return toReturn