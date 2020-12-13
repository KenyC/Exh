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
	return A("x", domain = domain)

def Ay_in_(domain):
	return A("y", domain = domain)

def Az_in_(domain):
	return A("z", domain = domain)

def Ex_in_(domain):
	return E("x", domain = domain)

def Ey_in_(domain):
	return E("y", domain = domain)

def Ez_in_(domain):
	return E("z", domain = domain)