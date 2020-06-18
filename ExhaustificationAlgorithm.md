
Exhaustification algorithm
===============================

The algorithm used by this package is described here, with a proof of correction.

# Definitions

Write $p$ for the prejacent, and $\mathcal A$ the set of alternatives. 

**Definition:** A set of alternative $\mathcal A'$ is consistent with the prejacent iff $p \wedge \bigwedge_{q\in\mathcal A'}\neg q$ is consistent.

**Definition:** A set of alternative $\mathcal A'$ is maximal iff it is consistent with the prejacent and there is no set $\mathcal A'\subsetneq \mathcal A''$ consistent with the prejacent.

**Definition:** A world *w* is minimal if *p* is true in *w* and there is no other world $w'$ such that the set of alternatives false in $w'$ strictly contains the set of alternatives false in $w''$.
**Definition** An alternative $q\in\mathcal A$ is innocently excludable (*IE*) iff it belongs to every maximal set of alternatives.

# Description of the algorithm
  1. Find, for every minimal world $w$, the set of alternatives false in $w$.
      a. Initialize an empty list $L$ of boolean arrays of length $\#\mathcal A$.
      b. For each world $w$ true of $p$, add the array $v_i$ - which maps $i$ to true if alternative $a_i$ is true in $w$ - if there isn't a vector with more false values in $L$.
      c. By construction, the list $L$ contains, for every minimal world $w$, the set of alternatives false in $w$.
  2. The IE alternative are the intersection of the vectors in $L$.

# Proof of correction

**Claim:** The set of alternatives false in a minimal world is a maximal set. Reciprocally, every maximal set is the set of false alternatives in a minimal world.
**Proof:** 
If $w$ is a world where $p$ is true, call $alt(w)$ the set of alternatives false in $w$. Now, if $w$ is a minimal world, then for all worlds $w'$, $alt(w')$ does not strictly contain $alt(w)$. In other words there is no set of alternatives $\mathcal A'$ such that $p \wedge \bigwedge_{q\in\mathcal A'}\neg q$ is consistent. But this is just saying that $alt(w)$ is maximal.
Reciprocally, if $\mathcal A'$ is a maximal set and $w$ a world where $p \wedge \bigwedge_{q\in\mathcal A'}\neg q$ is true, then $w$ is minimal. If $w$ weren't, then we could find a world $w'$ where $p$ is true and a bigger set of alternatives $\mathcal A''$ than $\mathcal A'$ is false. But then $\mathcal A'$ wouldn't be maximal.

**Claim:** The set of alternatives false in every minimal worlds is the set of IE alternatives.
**Proof:** From the claim above, it follows that the set of maximal sets is the set $\left\lbrace alt(w)\ \middle|\ w\text{ is a minimal world}\right\rbrace$. Therefore, the set of alternatives false in every minimal world is the set of alternatives in every maximal set, i.e. the IE alternatives.

