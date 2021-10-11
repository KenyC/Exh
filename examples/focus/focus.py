# %%
"""
# Setting custom domain sizes

Version > 1.1 is required. It should be available on PyPI or from GitHub directly.
Focus is an extension and must be activated by importing it after importing "exh".
"""

import exh
from exh import *
from exh.exts.focus import *
print(exh.__version__)

# %%
"""
Focus allows you to give stipulated alternatives to specific constituents.
Use the constructor "Focus" to put focus on apple.
"""

apple      = Pred(name = "apple")
cantaloupe = Pred(name = "cantaloupe")

# Creating sentence where "apple" is focused and has "cantaloupe" as an alternative
prejacent = Focus(apple, alts = [cantaloupe]) 

# A focused constituent is printed with F subscript
jprint(prejacent)

# %%
"""
In the absence of exhaustivity operators, a focused element behaves just like its unfocused counterpart.
"""

focused   = Focus(apple, alts = [cantaloupe]) & Focus(cantaloupe, alts = [apple])
unfocused = apple & cantaloupe

universe = Universe(fs = [focused, unfocused])

print(
	"Are focused and unfocused formulas are equivalent?",
	universe.equivalent(focused, unfocused)
)

# %%
"""
However, focused and unfocused constituents don't give rise to the same alternatives. 
This can be seen when applying Exh.
"""

exh1 = Exh(focused)
exh2 = Exh(unfocused)

# all alternatives obtained by replacing ans simplifying the conjunction
# + replacing conjuncts by their focused alternatives
jprint(exh1.alts)
# all alternatives obtained by replacing ans simplifying the conjunction
jprint(exh2.alts)

# %%
"""
**Caveat:** the same predicate can appear focused in one place with a set of alternatives S, unfocused somewhere else,
focused with a different set of alternatives S' in some other place. Each occurrence behaves as it is specified: 
the first occurence has S as alternatives, the second nothing, the third S'.
"""

kiwi = Pred(name = "kiwi")
f = Focus(apple, alts=[cantaloupe]) | apple | Focus(apple, alts=[kiwi])
jprint(Exh(f).alts)

