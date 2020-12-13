# %%
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

# %%
from exh import *
from exh.exts.subdomain import *
from exh.model import options # for fancy displays

options.latex_display = False


d    = Pred(name = "d", depends = "x")
mask = np.array([True, False, True])
f    = SubdomainExistential("x", d, mask = mask)

assert(f.evaluate(d = [True, False, False]))
assert(not f.evaluate(d = [False, True, False]))

f = Ec_x > d
assert(f.evaluate(d = [True, False, False]))
assert(not f.evaluate(d = [False, False, False]))

# %%
assert(f.display_aux(latex = False) == "\u2203\u02da\u02da\u02da x, d(x)")

# %% Test alternative formation

masks_alt = np.stack([alt.mask for alt in f.all_alternatives()])
# print(masks_alt)
assert(np.all(masks_alt == [
	[ True, False, False],
    [False,  True, False],
 	[ True,  True, False],
 	[False, False,  True],
	[ True, False,  True],
 	[False,  True,  True]
]))

f_    = SubdomainExistential("x", d, mask = np.array([True, False, True]))
masks_alt = np.stack([alt.mask for alt in f_.lower_alternatives()])
# print(masks_alt)
assert(np.all(masks_alt == [
	[ True, False, False],
 	[False, False,  True]
]))

# %%
g = Exh(f, alts = list(f.lower_alternatives()), ii = True)
h = Exh(f, alts = list(f.lower_alternatives()), ii = False)
universe = Universe(f = g)
assert(universe.equivalent(g, Ax > d))
assert(universe.equivalent(h, f))


g = Exh(f, scales = sub_scale, ii = True)
h = Exh(f, scales = dom_scale, ii = False)
g.diagnose(print)
universe = Universe(f = g)
assert(universe.equivalent(g, Ax > d))
assert(universe.equivalent(h, f))



# %%

