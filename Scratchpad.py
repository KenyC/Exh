#!/usr/bin/env python
# coding: utf-8

# # This notebook is used for testing

# %%


import numpy as np

from exh import *

# %%

a = Pred(1, name = "a", depends = "x")
b = Pred(2, name = "b", depends = "x")


# %%

print(((Ex > a("y")) & b).free_vars)


# %%