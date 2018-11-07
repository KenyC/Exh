import numpy as np

def entails(a, b):
	return np.all(np.logical_or(np.logical_not(a), b))