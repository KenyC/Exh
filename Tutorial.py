#!/usr/bin/env python
# coding: utf-8

# # Tutorial 

# ## Imports

# %%


from exh import *
from exh.utils import jprint # for fancy displays


# ## Create formulas
# 
# Formulas are created from propositions (0-ary predictates) and predicates. Predicates have indices, such that predicates with the same index always have the same truth-value and predicates with different indices are logically independent. Here is a code to create a predicate with index 4.

# %%


d = Pred(4, name = "d") 
d1 = Pred(7) # "name" is optional, "name" makes prettier display with print and helps for evaluation of formulas


# By default, *exh.formula* creates 3 propositions a,b and c with indices 0, 1, 2 respectively. Once some propositions are defined, one can create complex formulas with & (and), | (or) and \~ (not).

# %%


# f1: a or b
f1 = a | b
jprint(f1)

# f2: a and b
f2 = a & b
jprint(f2)

# f3: a or (not a and b)
f3 = a | (~a & b)
jprint(f3)


# To turn a proposition into a n-ary predicate (for use in quantified formulas), one needs to specify the number of variables it depends on. Optionally, one may indicate which varaible the predicate depends on by default. That way, we don't need to specify the dependencies in formulas

# %%


d.depends(1) # Making a unary predicate

# Alternatively, making a unary predicate with a default variable name
d.depends("x")


# Once this is done, one can use the following syntax to create a universal statement.  A("x") creates a quantifier over "x", which combines with ">" and a formula to form a quantified formula.

# %%


# f4: for all x, d(x)
f4 = A("x") > d
jprint(f4)
# If we want to mark explicitly or override the varaibles that d depends on, we write
# f4 = A("x") > d("x")


# Two simplifying tips:
#  - Existential and universal quantifiers over x, y, z are created by default under the names Ax, Ey, etc.
#  - If v is propositional variable, v("x") returns v and sets v to depend on x
# 
# Most straigthforwardly, one can create a quantified formula as follows:

# %%


# f5: there exists y, d(y)
f5 = Ey > d1("y") # a warning is displayed, because we hadn't specified that "d1" was a predicate
jprint(f5) # displays as A7 because we haven't given d1 a name


# ## Evaluate formulas
# The simplest way to evaluate a formula uses the method *evaluate* and the predicates' names.

# %%


# Evaluate f1 with a True and b True.
value = f1.evaluate(a = True, b = False)
jprint("'{}' is {}".format(f1, value))


# In quantified formulas, one needs to provide as many values for a predicate as there are individuals in the domain. The number of individuals in the domain is set in *options.py* and defaults to 3. The three values are provided as a list.

# %%


# Evaluate f4 with d(0) True, d(1) True and d(2) True
value = f4.evaluate(d = [True, True, True])
jprint(f4, " is ", value)


# One may sometimes want to evaluate a formula against all possible assignments of truth-values. To do that, one constructs a *Universe* object. This object constructs all possible assignments of truth-values to propositions and predicates within a given set of formulas, passed as an argument to the universe constructor. The *truth_table* method displays the evaluated formula in a fancy chart.

# %%


from exh.worlds import Universe

# A Universe can be created from formulas ; 
# the constructor extracts all the independent predicates and propositions and creates all possible logical possibilities
prop_universe = Universe(fs = [a, b, c])

print(prop_universe.evaluate(f1, f2, f3))
prop_universe.truth_table(f1, f2, f3)


# Universes come with methods to check standard logical relations: entailment, equivalence and consistency

# %%


# The first three propositions entail that "not a" and "b", contradicting the fourth. 
value = prop_universe.consistent(a | b,
                                 ~a | ~b,
                                 b | ~a,
                                 a | ~b)
print(value)

value = prop_universe.entails(a | ~ b & c,
                              ~(b & ~a) )
# NB: "a | b & c"  is parsed as "a | (b & c)"

print(value)

# De Morgan's law
value = prop_universe.equivalent(~a | ~c,
                                ~(a & c) )
print(value)


# ## Exhaustification

# Exhaustification can be computed against a set of stipulated alternatives.
# 
# **NB:** Innocent exclusion is computed upon creation of the object, expect slowdowns if number of worlds is big.

# %%


e = Exh(Ex > d, alts = [Ax > d])
e1 = Exh(a | b, alts = [a, b, a & b])


# The program does not give you a representation of what *h* is, but one can confirm the result in a couple of ways: first, the method *diagnose* gives us the innocently excludable alternatives. Second, like any formula, we can evaluate *e* and check that it behaves like "some but not all". Third, we can create a *Universe* object and check for equivalence with en explicit "some but not all" formula.

# %%


e.diagnose()
e1.diagnose()

quant_universe = Universe(fs = [e])
print()
quant_universe.truth_table(e, (Ex > d) & ~(Ax > d))


print()
print("Is e equivalent to 'some but not all'?")
print(
    quant_universe.equivalent(
    e,
    (Ex > d) & ~(Ax > d)
    ))


# Below is a more involved example with more alternatives:

# %%


# constructing new predicates and immediately indicating dependency in x
p1 = Pred(5, name = "p1", depends = ["x"]) 
p2 = Pred(6, name = "p2", depends = ["x"])

prejacent = Ax > p1 | p2

exh = Exh(prejacent, alts = [Ax > p1 & p2,
                             Ax > p1,
                             Ax > p2,
                             Ex > p1 & p2,
                             Ex > p1,
                             Ex > p2])
exh.diagnose()
# Reads like "none of them did both p1 and p2" ; an embedded implicature
# What if we didn't have existential alternatives?

exh2 = Exh(prejacent, alts = [Ax > p1 & p2,
                              Ax > p1,
                              Ax > p2])
exh2.diagnose()
universe = Universe(fs = [exh2])
print(universe.entails(exh2, Ex > p1 & ~p2))
print(universe.entails(exh2, Ex > p2 & ~p1))
# Two implicatures: 1) that someone did only p1, 2) that someone did only p2


# ### Automatic alternatives

# When not specified, the alternatives to the prejacent are computed in a Katzirian manner: all alternatives are considered that can be obtained from the prejacent by sub-constituent and scalar substitutions. Which alternatives were obtained by this process can be probed after the object is constructed.

# %%


h2 = Exh (a | b | c)
jprint("Computed alternatives", h2.alts)


# It is possible to specify the scales, to decide whether to allow substitution by sub-consituent.

# %%


h3 = Exh(a | b | c, subst = False) # no replacement by sub-constituent allowed (only scalar alternatives)
jprint(h3.alts)

h4 = Exh(Ex > p1 | p2, scales = [{Or, And}]) # no "some", "all" scale
jprint(h4.alts)
# NB: to avoid unbound variables, the quantifier's scope is not considered a sub-consituent of the quantifier


# %%


h3.diagnose()
h4.diagnose()


# ## Advanced usage

# ### Formulas with multiple quantifiers

# One can create multiply quantified sentences ; the number of worlds grows exponentially. One predicate that depends on two variables will give rise to 9 independent variables ; we get 2^9 = 512 worlds.

# %%


p3 = Pred(13, name = "p3")
prejacent = Ex > Ay > p3("x", "y")

e = Exh(prejacent, alts = [Ay > Ex > p3, Ax > Ey > p3, Ey > Ax > p3])
e.diagnose()


# ### Recursive exhaustification
# 
# The object *Exh* is just like any other formula. It can be embedded, yielding recursive exhaustification. Here is for instance a replication of free choice:

# %%


# For fancy html display
from IPython.core.display import display, HTML

prejacent = Ex > p1 | p2 # The existential quantifier can be thought of as an existential modal

free_choice = Exh(Exh(prejacent, scales = []), scales = []) 
# no scalar alternatives  for the moment

# Let's see what has been computed
# First, the alternatives
print("Alternatives:")

to_display = "<ul>"
for alt in free_choice.alts:
    to_display += "<li>{}</li>".format(alt)
to_display += "</ul>"
display(HTML(to_display))

# Second, the innocently excludable alternatives
free_choice.diagnose()
# The result seems right ; let's check entailments

fc_universe = Universe(f = free_choice) # one can use f you only have one formula
print("Am I allowed to do p1?")
print(fc_universe.entails(free_choice, Ex > p1))
print("Am I allowed to do p2?")
print(fc_universe.entails(free_choice, Ex > p2))

# We have weak FC ; what about strong free-choice?
print("Does the sentence say that I can do p1 without doing p2?")
print(fc_universe.entails(free_choice, Ex > p1 & ~p2)) # We don't have strong FC
print("Is the sentence compatible with a requirement to do both p1 and p2?")
print(fc_universe.consistent(free_choice, Ax > p1 & p2))

# Can we derive strong FC with universal scalar alternatives?
someall = [{Existential, Universal}] # we only allow some/all scale, not or/and scale
fc_2 = Exh(Exh(prejacent, scales = someall), scales = someall) 

to_display = "<ul>"
for alt in fc_2.alts:
    to_display += "<li>{}</li>".format(alt)
to_display += "</ul>"
display(HTML(to_display))

fc_2.diagnose()

print("Does the sentence say that I can do p1 without doing p2?")
print(fc_universe.entails(fc_2, Ex > p1 & ~p2)) # We don't have strong FC
print("Is the sentence compatible with a requirement to do both p1 and p2?")
print(fc_universe.consistent(fc_2, Ax > p1 & p2))

# One may wonder by sub-constituent replacement, "Ex, p1(x)" is not an alternative to "Exh(Ex, p1(x) or p2(x))"
# If this were so, note that free choice wouldn't be derived.
# "exh" is set to not be removable by sub-constituent replacement (you can modify this in *options.py*)


# ### Innocent inclusion

# *Exh* can also compute innocent inclusion. 

# %%


# Strengthening to conjunction, when scalar alternatives are absent
print("### DISJUNCTION ###")
conj = Exh(a | b, scales = [], ii = True) # ii parameter for innocent inclusion
conj.diagnose()

print("### FREE CHOICE ###")
fc_ii = Exh(Ex > p1 | p2, ii = True) # Automatic alternatives
fc_ii.diagnose()

print("Allowed to do p1 not p2:", fc_universe.entails(fc_ii, Ex > p1 & ~p2))
print("Allowed to do p2 not p1:", fc_universe.entails(fc_ii, Ex > p2 & ~p1))
print("Allowed to do both:", fc_universe.consistent(fc_ii, Ex > p2 & p1))


# %%




