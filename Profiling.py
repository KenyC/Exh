# run with 
# kernprof --line-by-line Profiling.py
# python -m line_profiler Profiling.py.lprof
# %%

from exh import *

# %%

a = Pred(0, name = "a", depends=["x", "y"])

# %%
(Ex > Ay > a).evaluate(a = [[True, False, False], [False, True, False], [False, False, True]])
