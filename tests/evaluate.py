# %%
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

# %%
from exh import *

d = Pred(name = "d", depends = "x", domains = [Domain(5)])
e = Pred(name = "e", depends = ["x", "y"], domains = [Domain(2), Domain(3)])

d.evaluate_aux(
	vm         = d.vars()
	assignment = np.array([True, False, True])
	d = [True, False, True, False, True])





# %%

