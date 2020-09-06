import numpy as np

def convert_to_base(number, base):
	digits = []
	current_number = number

	while current_number != 0:
		rest, current_number = current_number % base, current_number // base
		digits.append(rest)

	digits.reverse()

	if not digits:
		digits = [0]

	return digits

def get_many_valued_assignment(n_vars, n_truth_values = 3):

	def pad_with_zeroes(l, n):
		length = len(l)
		return (n - length) * [0] + l

	assignment_generator = list(map(
		lambda x: pad_with_zeroes(convert_to_base(x, base = n_truth_values), n_vars), 
		range(n_truth_values ** n_vars)
	))

	return np.array(assignment_generator)