# %%
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

# %%
from exh import *
from exh.exts.focus import *


# %%
"""
# Construction and evaluation
"""

f = Focus(a | b, [b])

assignment = np.array([
	[True,  True], 
	[True,  False], 
	[False, True], 
	[False, False]
])

assert((f.evaluate_aux(
	vm         = f.vars(),
	assignment = assignment,
	variables  = {}
) ==
(a | b).evaluate_aux(
	vm = f.vars(),
	assignment = assignment,
	variables  = {}
)).all()
)

assert(not (f.evaluate_aux(
	vm         = f.vars(),
	assignment = assignment,
	variables  = {}
) ==
(a & b).evaluate_aux(
	vm = f.vars(),
	assignment = assignment,
	variables  = {}
)).all()
)

# %%
"""
# Alternative calculation
"""

scale = FocusScales()


assert(
	scale.alternatives_to([f])
	== [b]
)

assert(
	scale.alternatives_to([f])
	!= [a | b]
)

# %%
"""
# Exhaustification
## Simple cases
"""

# Test if FocusScales is now default (importing the extention should make it default)
assert(any(isinstance(s, FocusScales) for s in Exh(a).e.scales.scales))

# %%

g = Focus(a, alts = [b, c])
exhg = Exh(g, scales = FocusScales())

assert(
	exhg.alts == [
	  g, 
	  b,
	  c
	]
)

universe = Universe(f = exhg)
assert(universe.equivalent(exhg, a & ~b & ~c))

# %%

g = Focus(a | b, alts = [a & b])
exhg = Exh(g, scales = FocusScales())

assert(
	exhg.alts == [
	  g, 
	  Focus(a, alts=[a & b]), 
	  Focus(b, alts=[a & b]), 
	  a & b
	]
)

universe = Universe(f = exhg)
assert(universe.equivalent(exhg, (a | b) & ~(a & b)))


# %%
"""
## Exhaustification across operators
"""

apple      = Pred(name = "A", depends = ["x"])
cantaloupe = Pred(name = "C", depends = ["x"])

h = Ex > Focus(apple, alts = [cantaloupe])

exhh = Exh(h, scales = FocusScales())

complex_universe = Universe(f = h)

assert(complex_universe.equivalent(
	exhh,
	(Ex > apple) & ~(Ex > cantaloupe)
))

assert(not complex_universe.equivalent(
	exhh,
	Ex > apple
))

# %%
"""
Not A
"""

prop_universe = Universe(fs = [a, b, c])

exhf = Exh(~Focus(a, alts = [c]), scales = FocusScales(), subst = False)

assert(exhf.alts == [~Focus(a, alts = [c]), ~c])

assert(prop_universe.equivalent(
	exhf,
	~a & c
))

# %%
"""
Recursive exh
""" 

prej    = Focus(a, alts = [c])
fst_exh = Exh(prej, scales = FocusScales())
snd_exh = Exh(fst_exh, scales = FocusScales ())

assert(
	fst_exh.alts ==
	[prej, c]
)
assert(
	snd_exh.alts ==
	[Exh(prej), Exh(c)]
)

assert(prop_universe.equivalent(
	snd_exh,
	a & ~c
))


# %%
