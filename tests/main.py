# This file must run fully without exceptions
# %%
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

# %%
hashes = "#####################################################"
def header(title):
    title = " {} ".format(title)
    padding_size = len(hashes) - len(title)
    print(hashes[:padding_size // 2] + title + hashes[-padding_size // 2:])


# %%
header("IMPORTS")
from exh import *
from exh.model import options # for fancy displays

options.latex_display = False


# %%
header("FORMULA CONSTRUCTION AND DISPLAY")

# Index-less formulas, testing increment index
last_index = Pred().idx
assert(Pred(name = "george").idx == last_index + 1)

# Index formula
Pred(4, name = "d") 
Pred(7) # "name" is optional, "name" makes prettier display with print and helps for evaluation of formulas
Pred(2, name = "er", depends = 1)
Pred(2, name = "er", depends = ["x", "y"])
Pred(2, name = "er", depends = "x")


a | b
a & b
print(a | (~a & b))


d = Pred(4, name = "d")
e = Pred(5, name = "e")

d.depends(1) # Making a unary predicate
d.depends("x")
e.depends("x", "y")


f4 = A("x") > d
print(f4)
A("x") > Ey > e 
f5 = Ax > Ey > e("y", "x")


# names for nameless predicates
assert(Pred(7).display_aux(False) == "A7")
assert(a.display_aux(False)       == "a")

# Display test
options.latex_display = True
assert(f4.display() == r"$\forall x, d(x)$")
options.latex_display = False
assert(f4.display() == "\u2200 x, d(x)")

# %%
header("FORMULA METHODS")

# Simple prop logic formul
assert(not (a == b))
assert((a | b) == (b | a))
assert(not ((a | b) == (b | c)))
assert((a | b) != (a & b))

# FOL formulas
assert((Ex > Pred(4, "d1", depends = "x")) == (Ex > d))


# %%
header("EVALUATION")
# Propositional logic

assert((a | b).evaluate(a = True, b = False))
assert((a | (b & ~a)).evaluate(a = True, b = False))

# %%
# FOL

assert((Ax > d("x")).evaluate(d = [True, True, True]))

assert((Ax > Ey > e("y", "x")).evaluate(e = [
                                       [True, True, False],
                                       [False, False, False],
                                       [False, False, True]
                                       ]))





# %%
header("UNIVERSE")

prop_universe = Universe(fs = [a, b, c])
assert(prop_universe.n == 3)

prop_universe = Universe(fs = [a & b, b | ~ a])
assert(prop_universe.n == 2)

import exh.model.options as options
dom_quant = options.dom_quant

prop_universe = Universe(fs = [Ax > d("x"), Ax > Ey > e("y", "x")])
assert(prop_universe.n == dom_quant + dom_quant**2) 


prop_universe = Universe(fs = [a, b, c])
result = np.array(
      [[False, False,  True],
       [False,  True, False],
       [False,  True,  True],
       [ True,  True, False],
       [False, False,  True],
       [False,  True,  True],
       [False,  True,  True],
       [ True,  True,  True]]
)
assert(np.all(prop_universe.evaluate(a & b, a | b, ~a | c ) == result))



value = prop_universe.consistent(a | b,
                                 ~a | ~b,
                                 b | ~a,
                                 a | ~b)
assert(not value)

value = prop_universe.entails(a | ~ b & c,
                              ~(b & ~a) )
# NB: "a | b & c"  is parsed as "a | (b & c)"

assert(value)

# De Morgan's law
value = prop_universe.equivalent(~a | ~c,
                                ~(a & c) )
assert(value)

quant_universe = Universe(fs = [Ex > d])
quant_universe.truth_table((Ex > d) & ~(Ax > d), html = False)


# %%
header("EXHAUSTIFICATION")


e = Exh(Ex > d, alts = [Ax > d])
e1 = Exh(a | b, alts = [a, b, a & b])

# Test syntactic equality
assert(e1 == Exh(b | a, alts = []))
assert(e1 != Exh(b | c, alts = []))


assert(
    prop_universe.equivalent(
    e1,
    (a | b) & ~(a & b)
    ))



assert(
    quant_universe.equivalent(
    e,
    (Ex > d) & ~(Ax > d)
    ))




p1 = Pred(5, name = "p1", depends = ["x"]) 
p2 = Pred(6, name = "p2", depends = ["x"])

prejacent = Ax > p1 | p2

exh = Exh(prejacent, alts = [Ax > p1 & p2,
                             Ax > p1,
                             Ax > p2,
                             Ex > p1 & p2,
                             Ex > p1,
                             Ex > p2])

quant_universe = Universe(f = prejacent)

assert(quant_universe.equivalent(exh, Ax > (p1 | p2) & ~ (p1 & p2)))


exh2 = Exh(prejacent, alts = [Ax > p1 & p2,
                              Ax > p1,
                              Ax > p2])

assert(quant_universe.equivalent(exh2, prejacent & (Ex > ~p1) & (Ex > ~p2)))
assert(not quant_universe.equivalent(exh2, prejacent & (Ex > p1) & (Ex > p2)))


# Two implicatures: 1) that someone did only p1, 2) that someone did only p2

# Dealing with free_vars
Exh(p1, alts = [p1, p2])
Ex > Exh(p1, alts = [p1, p2])


# ### Automatic alternatives

# When not specified, the alternatives to the prejacent are computed in a Katzirian manner: all alternatives are considered that can be obtained from the prejacent by sub-constituent and scalar substitutions. Which alternatives were obtained by this process can be probed after the object is constructed.



h2 = Exh (a | b | c)
options.latex_display = False
print("Computed alternatives", h2.alts)

assert(len(h2.alts) == 4 + # subtree1 
                       1 + # subtree2
                       2 * 4 * 1) # alts for each subtree

# It is possible to specify the scales, to decide whether to allow substitution by sub-consituent.



h3 = Exh(a | b | c, subst = False) # no replacement by sub-constituent allowed (only scalar alternatives)
assert(len(h3.alts) == 2 * 2) # alts for each subtree


h4 = Exh(Ex > p1 | p2, scales = [{Or, And}]) # no "some", "all" scale
assert(len(h4.alts) == 2 + 2) 

# Dealing with free_vars without specified alternatives
Exh(p1 | p2)

# Dealing with recursive exh when the embedded exh has stipulated alternatives
h5 = Exh(Exh(a, alts = [a, b]))
assert(Exh(b, alts = [a]) in h5.alts)
assert(prop_universe.equivalent(h5, a & ~b))



# %%
header("FREE CHOICE REPLICATION")



prejacent = Ex > p1 | p2 # The existential quantifier can be thought of as an existential modal

free_choice = Exh(Exh(prejacent, scales = []), scales = []) 
# The result seems right ; let's check entailments

fc_universe = Universe(f = free_choice) # one can use f you only have one formula
assert(fc_universe.entails(free_choice, Ex > p1))
assert(fc_universe.entails(free_choice, Ex > p2))


# We have weak FC ; what about strong free-choice?
assert(not fc_universe.entails(free_choice, Ex > p1 & ~p2)) # We don't have strong FC
assert(fc_universe.consistent(free_choice, Ax > p1 & p2))

# Can we derive strong FC with universal scalar alternatives?
someall = [{Existential, Universal}] # we only allow some/all scale, not or/and scale
fc_2 = Exh(Exh(prejacent, scales = someall), scales = someall) 


assert(not fc_universe.entails(fc_2, Ex > p1 & ~p2)) # We don't have strong FC
assert(not fc_universe.consistent(fc_2, Ax > p1 & p2))

# %%
header("INNOCENT INCLUSION")


conj = Exh(a | b, scales = [], ii = True) # ii parameter for innocent inclusion
assert(prop_universe.equivalent(conj, a & b))

fc_ii = Exh(Ex > p1 | p2, ii = True) # Automatic alternatives

assert(fc_universe.entails(fc_ii, Ex > p1 & ~p2))
assert(fc_universe.entails(fc_ii, Ex > p2 & ~p1))
assert(not fc_universe.consistent(fc_ii, Ex > p2 & p1))


# %%

header("EXTENSION : GENERALIZED QUANTIFIER")

# Import and check import
from exh.exts.gq import *
Mx



# Construct formula
f = Mx > p1

# Check if the options set for the main module also apply to the extension
options.latex_display = True
assert(f.display() == r"$\text{Most } x, p1(x)$")
options.latex_display = False
assert(f.display() == "Most  x, p1(x)")

# Test formula construction
Mx > p1
Exactly(3, "x") > p1
MoreThan(4, "x") > p1 | p2




# %%


