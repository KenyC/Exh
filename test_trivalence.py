# This file must run fully without exceptions
# %%
hashes = "#####################################################"
def header(title):
		title = " {} ".format(title)
		padding_size = len(hashes) - len(title)
		print(hashes[:padding_size // 2] + title + hashes[-padding_size // 2:])


# %%
header("IMPORTS")
from exh.exts.trivalence.prop import *
from exh.exts.trivalence.model import *
from exh.model import options # for fancy displays


options.latex_display = False


# %%
header("FORMULA CONSTRUCTION")


Pred(4, name = "d") 
Pred(7) # "name" is optional, "name" makes prettier display with print and helps for evaluation of formulas
Pred(2, name = "er", depends = 1)
Pred(2, name = "er", depends = ["x", "y"])
Pred(2, name = "er", depends = "x")
Named("a", a)
assert(Named("a", a, latex_name = "b").display_aux(latex = False) == "a")
assert(Named("a", a, latex_name = "b").display_aux(latex = True)  == "b")

a | b
a & b
print(a | (~a & b))

# %%
d = Pred(4, name = "d")
e = Pred(5, name = "e")

d.depends(1) # Making a unary predicate
d.depends("x")
e.depends("x", "y")



# names for nameless predicates
assert(Pred(7).display_aux(False) == "A7")
assert(a.display_aux(False)       == "a")

# %%
header("FORMULA METHODS")

# Simple prop logic formul
assert(not (a == b))
assert((a | b) == (b | a))
assert(not ((a | b) == (b | c)))
assert((a | b) != (a & b))


# %%
header("EVALUATION")
# Propositional logic

assert((a | b).evaluate(a = TVal.true, b = TVal.false) == TVal.true)
assert((a | b).evaluate(a = TVal.true, b = TVal.false) == Named("a_or_b", a | b).evaluate(a = TVal.true, b = TVal.false))
assert((a | (b & ~a)).evaluate(a = TVal.true, b = TVal.false) == TVal.true)

# %%

# Testing default strong Kleene behavior
assert((a | b).evaluate(a = TVal.pound, b = TVal.false) == TVal.pound)
assert((a | b).evaluate(a = TVal.true,  b = TVal.pound) == TVal.true)

assert((a & b).evaluate(a = TVal.pound, b = TVal.false) == TVal.false)
assert((a & b).evaluate(a = TVal.true,  b = TVal.pound) == TVal.pound)

# %%
# Testing changes in projection behavior
Formula.projection = ProjectionRules.WeakKleene
assert((a | b).evaluate(a = TVal.pound, b = TVal.false) == TVal.pound)
assert((a | b).evaluate(a = TVal.true,  b = TVal.pound) == TVal.pound)

assert((a & b).evaluate(a = TVal.pound, b = TVal.false) == TVal.pound)
assert((a & b).evaluate(a = TVal.true,  b = TVal.pound) == TVal.pound)
Formula.projection = ProjectionRules.StrongKleene


# %%

# Testing "with" environment
with WeakKleene():
	assert((a | b).evaluate(a = TVal.true,  b = TVal.pound) == TVal.pound)

# When something fails in the body of the "with" statement, the original projection rule should be restored
try:
	with WeakKleene():
		assert((a | b).evaluate(a = TVal.true,  b = TVal.pound) == TVal.false)
except Exception as e:
	assert(Formula.projection == ProjectionRules.StrongKleene)
else:
	raise Exception("Shouldn't evaluate to that!")


# %%

assert((Assert(a)).evaluate(a = TVal.pound) == TVal.false)
assert((Presupposition(a)).evaluate(a = TVal.false) == TVal.true)


# %%
header("UNIVERSE")

prop_universe = Universe(fs = [a & b, b | ~ a])
assert(prop_universe.n == 2)

prop_universe = Universe(fs = [a, b, c])
assert(prop_universe.n == 3)



# %%

value = prop_universe.consistent(
	a  | b,
	~a | ~b,
	b  | ~a,
	a  | ~b
)
assert(not value)
# %%
# Strawson entailment
value = prop_universe.entails(
	(~a) & Presupposition(b),
	Presupposition(a | b)
)

assert(value)

value = prop_universe.entails(
	a | b,
	a | b | c
)

assert(value)

# %%
# De Morgan's law
value = prop_universe.equivalent(
	~a | ~c,
	~(a & c) 
)
assert(value)

