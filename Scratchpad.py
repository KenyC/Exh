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

# %%

d = Pred(4, name = "d", n_ary = 1)

# %%

print(d.vm.n)

# %%

(Ax > d).evaluate_aux(np.array([[True, True, True]]), d.vm, {"x" : 1})

# %%


exh.formula

# %%





# %%


f = Mx > a
jprint(f)


# %%


from exh.worlds import Universe

u = Universe(f = f)

u.truth_table(f)


# %%


g = Exh(Mx > a | b)
u = Universe(f = g)


# %%


g.diagnose()


# %%


u.entails(g, ~(Mx > a))


# %%


u.vm.preds


# %%


g.vm.preds


# %%


print(u.vm.offset)
print(u.vm.names)
print(u.vm.preds)
print(u.vm.var_to_vm_index)


# %%


import itertools

for i in itertools.product(range(3), repeat = 0):
    print(i)


# %%


from table import *


# %%


t = Table()
t.set_header([12, True])
t.add_row([18798972, 12.989])
t.add_row(["zfefzeezf", "fzzef"])

t.print()

