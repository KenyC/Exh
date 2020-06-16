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

a = Pred(1, name = "a", depends = "x")
b = Pred(2, name = "b", depends = "x")


# %%
# Simple warm-up case

f1 = Ex > Exh(a, alts=[b])
print(f1)

# %%