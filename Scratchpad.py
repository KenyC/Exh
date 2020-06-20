#!/usr/bin/env python
# coding: utf-8

# # This notebook is used for testing

# %%

%load_ext autoreload

# %%
%autoreload 2

# %%


import numpy as np

from exh import *
from exh.model import options

options.latex_display = False

# %%

d = Pred(4, name="d", depends=["x", "y"])

(Ex > d).evaluate(d = [[True, False, True], 
                       [True, False, True], 
                       [False, True, False]])

# %%
f = Exh(a | b , alts = [a, b, a & b], ii = True)

f.diagnose(print)

# 
u = Universe(fs = [a, b])
u.truth_table(f, html = False)

# %%

uSPrejacent = u.restrict([1,2,3])
evalPosSet = [a, b, a&b]

# %%

maximalSets = alternatives.find_maximal_sets(uSPrejacent, evalPosSet)
print(maximalSets)

# %%

maximalInclSets = np.full((len(maximalSets), len(self.alts)), False, dtype = "bool")


# %%
# The maximal sets only refer to positions in the set of non-excludable alternatives
self.maximalInclSets = np.full((len(maximalSets), len(self.alts)), False, dtype = "bool")
self.maximalInclSets[:, np.logical_not(self.innocently_excl)] = maximalSets

self.innocently_incl_indices = np.prod(self.maximalInclSets, axis = 0, dtype = "bool")


# %%
from exh import alternatives

alternatives.find_maximal_sets(Universe(f = a), [a])

# %%