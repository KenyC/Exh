import numpy as np

def getAssignment(n):
	iterator = [np.array(2**(n-i-1)*(2**(i) * [False] + 2**(i) * [True]), dtype = "bool") for i in range(n)]
	return np.transpose(np.stack(iterator))
