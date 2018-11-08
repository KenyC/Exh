# Exh

## Imports

## Create formulas

Formulas are created from propositional variables. Variables have indices, such that variables with the same index always have a different truth-value and variables with different indices are logically independent. Here is a code to create a variable with index 4.

```python
d = Var(4)
```

By default, *formula.py* creates 3 variables a,b and c with indices 0, 1, 2 respectively. Once some variables are defined, one can create complex formulas with & (and), | (or) and \~ (not).


```python
f1 = a | b
f2 = a & b
f3 = a | (~a & b)
```

## Exhaust

The class *Exhaust* computes innocently excludable alternatives from a set of alternatives and a prejacent.

```python
# Computing innocently excludable alternatives for (a or b) when the alternatives are a, b and (a and b)
e = Exhaust(prejacent = a | b, alts = [a, b, a & b])
e.innocently_excludable()
# Returns [a & b]
```

If one leaves the alternative set unspecified, the *Exhaust* object defaults to the set of alternatives obtained by *scale substitution* and *sub-constituent*.

```python
e = Exhaust(prejacent = a | b)
e.innocently_excludable()
# Default alternatives: a, b, a & b
# Returns [a & b]
```
