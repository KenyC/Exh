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