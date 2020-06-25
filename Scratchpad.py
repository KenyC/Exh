#!/usr/bin/env python
# coding: utf-8

# # This notebook is used for testing

# %%


import numpy as np

from exh import *
from exh.model import options

options.latex_display = False

# %%

a = Pred(0, name = "a", depends=["x"])
b = Pred(1, name = "b", depends=["x"])

# %%

f = Ex > (Exh(a, alts = [b]) | Exh(b, alts = [a]))

# %%

c = Pred(2, name = "c", depends=["x", "y"])

f = Ex > Ey > c

# %%
u = Universe(f=f)

u.truth_table(f, html = False)

# %%

f1 = Exh(Ex > Exh(Ey > c))

f1.diagnose(print)

# %%

print(u.entails(f1, ~ (Ex > Ay > c)))
print(u.entails(f1, ~ (Ax > Ay > c)))
print(u.entails(f1, ~ (Ax > Ey > c)))
print(u.equivalent(f1, (Ex > (Ey > c) & ~ (Ay > c)) & ~ (Ax > Ey > c) & ~(Ex > Ay > c)))

# %%

u.truth_table(f, html = False)

# %%

print(u.equivalent(f, Ex > (a | b) & ~(a & b)))
print(u.consistent(f, ~ (Ex > a | b)))

# %%

g = Exh(Exh(f))

# %%

g.diagnose(print)

# %%
print(u.entails(g, 
               (Ex > a) & (Ex > b)
               ))
print(u.entails(g, 
               (Ex > a & ~b) & (Ex > b & ~a)
               ))
# print(u.consistent(g, Ax > a & ~b))


# %%