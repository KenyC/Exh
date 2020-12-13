# %%
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

# %%
from exh import *

d = Pred(name = "d", depends = "x", domains = [D5])
e = Pred(name = "e", depends = ["x", "y"], domains = [Domain(4), D3])

assert(d.evaluate_aux(
	vm         = d.vars(),
	assignment = np.array([[True, False, True, False, True]]),
	variables  = {"x" : 4}
))
assert(not d.evaluate_aux(
	vm         = d.vars(),
	assignment = np.array([[True, False, True, False, True]]),
	variables  = {"x" : 1}
))

	# d = [True, False, True, False, True])

# %%
assert((Ex_in_(D5) > d).evaluate(
	d = [True, False, True, False, True]
))
assert(not (Ex_in_(D4) > Ay_in_(D3) > e).evaluate(
	e = [
	[False, True, True],
	[True, False, True],
	[True, False, True],
	[True, False, True]
	]
))




# %%

