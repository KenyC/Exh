from .quantifier import *

A = quantifier_cons(Universal)
E = quantifier_cons(Existential)


Ax = A("x")
Ex = E("x")

Ay = A("y")
Ey = E("y")

Az = A("z")
Ez = E("z")




def Ax_in_(domain):
	return C(lambda formula: Universal("x", formula, domain))

def Ay_in_(domain):
	return C(lambda formula: Universal("y", formula, domain))

def Az_in_(domain):
	return C(lambda formula: Universal("z", formula, domain))

def Ex_in_(domain):
	return C(lambda formula: Existential("x", formula, domain))

def Ey_in_(domain):
	return C(lambda formula: Existential("y", formula, domain))

def Ez_in_(domain):
	return C(lambda formula: Existential("z", formula, domain))