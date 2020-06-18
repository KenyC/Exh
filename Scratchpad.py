#!/usr/bin/env python
# coding: utf-8

# # This notebook is used for testing

# %%


import numpy as np

from exh import *

# %%

a = Pred(0, name = "a", depends=["x", "y"])

# %%
import cProfile
cProfile.run((a).evaluate(a = [[True, False, False], [False, True, False], [False, False, True]]))

# %%


# %%
vm         = (a("x", "y", "z")).vm
assignment = np.random.choice(a=[False, True], size=(4, vm.n), p=[.5, .5])  
variables  = {"y" : 2, "z": 1}
free_vars  = ["x", "y"]

# %%
print(assignment)
assert(assignment.shape[1] == 3*3*3)

formula = a
from exh.model import options as option_quant
# %%
shape_output           = tuple(option_quant.dom_quant for _ in free_vars)
vars_not_in_assignment = set(formula.deps).difference(set(variables.keys()))

# %%
print(shape_output)
print(vars_not_in_assignment)

# %%
position_free_vars = np.full(len(free_vars), False)
for dep in vars_not_in_assignment: 
	position_free_vars[free_vars.index(dep)] = True #Potential for exception if free_vars is misconfigured
# %%
print(position_free_vars)

# %%

value_slots    = np.full(len(formula.deps), 0,     dtype = "int") 
mask_free_vars = np.full(len(formula.deps), False, dtype = "bool") 

for i, dep in enumerate(formula.deps):
	if dep in variables:
		value_slots[i]    = variables[dep]
	else:
		mask_free_vars[i] = True

# %%
print(value_slots)
print(mask_free_vars)
# %%

output = np.full((len(assignment), *shape_output), True, dtype = "bool")
grid   = np.indices(shape_output) 

for indices in np.ndindex(shape_output):
	value_slots[mask_free_vars] = np.array(indices)[position_free_vars]
	indexing = slice(len(assignment)), *indices
	output[indexing] = assignment[:, vm.index(formula.idx, value_slots)]

# %%
print(output[1, 2, :])
# val
# %%

value_slots[mask_free_vars] = np.array((5, 4))[position_free_vars]

# %%
print(value_slots)
# %%
position_free_vars

# %%
f = Exh(a | b , alts = [a, b, a & b])

# 
u = Universe(fs = [a, b])
u.truth_table(f, html = False)

# %%
f.e.u.evaluate(f.e.p).shape

# %%
from exh import alternatives

alternatives.find_maximal_sets(Universe(f = a), [a])

# %%

isinstance(sorted({2,1,5}), list)


# %%