#!/usr/bin/env python
# coding: utf-8

# # This notebook is used for testing

# %%


import numpy as np

from exh import *

# %%


# %%

<<<<<<< HEAD
print(((Ex > a("y")) & b).free_vars)

=======
f1 = Exh(Universe(fs = [a, b]), alts=[b])
print(f1)
>>>>>>> master

# %%

a.evaluate(assignment = [True], vm =a.vm)

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