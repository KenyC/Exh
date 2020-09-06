import numpy as np

import exh.prop.predicate as bivalent
from exh.exts.trivalence.model.truth import TVal
from .formula import Formula

class Pred(Formula, bivalent.Pred):
	"""
	Class for atomic proposition and predicate variable
	Attributes:
		- name : name for display and evaluation
		- arity : for n-ary predicates, the number of variables that the predicate depends on
		- deps : the name of the default variables that the predicate depends 
		(i.e. when no vars are specified, as in Ax > a, this is what the predicate depends on)
		- idx : an integer that uniquely identifies the predicate
	"""
	pass