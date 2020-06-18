from .formula   import *
from .predicate import *

true  = Truth()
false = Falsity()


a = Pred(0, name = "a")
b = Pred(1, name = "b")
c = Pred(2, name = "c")


if __name__ == "__main__":
	f1 = a & b & ~c
	f2 = a | b & c
