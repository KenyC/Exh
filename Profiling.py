"""
Using "line_profiler" by Robert Kern 

	pip install line_profiler

Steps to use

1) Decorate the function you wish to profile with "@profile"

	@profile
	def f():
		for i in range(1e6):
			pass
		return

2) Create the profiling file with the following command (tracks dependencies of the code afaiu):

	kernprof --line-by-line Profiling.py

3) Run the profiler using the following command

	python -m line_profiler Profiling.py.lprof
"""
# %%

from exh import *

# %%

p = Pred(0, name = "p", depends=["x"])
q = Pred(0, name = "q", depends=["x"])
r = Pred(0, name = "r", depends=["x"])

Exh(Exh(Exh(p | Exh(Exh(q)))) | Exh(r))


# %%
(Ex > Ay > a).evaluate(a = [[True, False, False], [False, True, False], [False, False, True]])
