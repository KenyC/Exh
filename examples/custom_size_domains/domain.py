# %%
"""
# Setting custom domain sizes

Version > 1.0 is required. It should be available on PyPI or from GitHub directly
"""

import exh
from exh import *
print(exh.__version__)

# %%
"""
To create a custom domain of quantification, use the following:
"""

D7 = Domain(7) # domain of size 7

# %%
"""
To use it, you need to define your predicates accordingly.
Specify the name of the variables that the predicate depends on in the ``depends`` parameter, and a corresponding list of domain.

**Notes:**
   - In version 1.0, you can but do not need to specify an index. Each new created predicate will get a new unique index.
   - The argument ``domains`` need not be provided, in which case the domains will all be ``default_domain``. The behavior of the predicate will then be exactly the same as in versions < 1.0.
"""
apple = Pred(
	name    = "apple", 
	depends = ["x"], 
	domains = [D7] # the variable "x" ranges over D7
)


eat = Pred(
	name    = "eat", 
	depends = ["x", "y"], 
	domains = [D7, default_domain] # the variable "x" ranges over D7 ; y over a default domain whose size is bound to ``exh.model.options.domain_quant``
)

# %%
"""
Quantifiers must also be adjusted. You can use ``Ex_in_``, ``Az_in_", etc., to create a quantifier that ranges over a custom domain.
"""

f = Ex_in_(D7) > apple
g = Ay > Ex_in_(D7) > eat


# %%
"""
Keep in mind that large domains incur large cost. For instance, even just the following starts to reach the limit of the reasonable:
"""
pear = Pred(
	name    = "pear", 
	depends = ["x"], 
	domains = [D7] # the variable "x" ranges over D7
)
f = Ex_in_(D7) > apple | pear
universe = Universe(f = f)
print("Number of worlds:", universe.n_worlds, "= 2^(7+7)")

# For 3 predicates:
print("3 predicates over D7:", 2 ** (7 * 3)) # 2M